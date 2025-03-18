<template>
<div>
    <h1 class="text-center">ระบบการจัดการหลักสูตร</h1>
    <button v-if="user.is_staff" type="button"
            class="btn btn-primary m-2 fload-end"
            data-bs-toggle="modal"
            data-bs-target="#edit-info-modal"
            @click="addClick()">
         Add Curriculum
    </button>

    <vue-good-table ref="curriculum-vgt" :columns="vgtColumns" :rows="curriculums"
            :select-options="{ enabled: false, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 20,
                setCurrentPage: 1,
            }">
            <div slot="table-actions">
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        columns
                    </button>

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="column.label +'-'+index" href="#">
                            <span href="#" class="small" tabIndex="-1" @click.prevent="toggleColumn(index, $event)">
                                <formulate-input type="checkbox" v-if="!column.hidden" disabled="true"
                                    checked="true"></formulate-input>
                                {{ column.label }}
                            </span>
                        </a>
                    </div>
                </div>
            </div>

            <template slot="table-row" slot-scope="props">
                <span v-if="props.column.field === 'action'">
                    <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="viewClick(props.row)">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button v-if="
                        user.is_staff 
                        
                    " type="button" :id="'edit-button-' + props.row.id" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="
                        user.is_staff 
                    " type="button" @click="deleteClick(props.row.id)" class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>
    
    <div class="modal fade" id="edit-info-modal" ref="curriculum-edit-info-modal"
        tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false" 
        aria-labelledby="edit-info-modal-label" aria-hidden="true">

        <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content">

                <div class="modal-header">
                    <h5 class="modal-title" id="edit-info-modal-label">{{ modalTitle }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>

                <div class="modal-body">

                    <div class="d-flex flex-row bd-highlight mb-3">

                        <div class="p-2 w-50 bd-highlight">
                            <button v-if="!addingNewCurriculum" type="button" class="btn btn-primary m-2 fload-end" @click="showCurriculumStudentModal=true;"
                                data-bs-toggle="modal" data-bs-target="#edit-info-modal">
                                Show Students
                            </button>
                            
                            <FormulateForm name="curriculum-formulate-form-1" ref="curriculum-formulate-form-1">
                                <formulate-input ref="curriculum-formulate-form-1-th_name" type="text" v-model="curriculum.th_name"
                                        label="Thai Name" validation="required|max:50"
                                        :readonly="modalReadonly || !formRender.edit.th_name"></formulate-input>
                                <formulate-input ref="curriculum-formulate-form-1-en_name" type="text" v-model="curriculum.en_name"
                                    label="English Name" validation="required|max:50"
                                    :readonly="modalReadonly || !formRender.edit.en_name"></formulate-input>
                                <FormulateInput
                                    ref="curriculum-formulate-form-1-start_date"
                                    type="date"
                                    v-model="curriculum.start_date"
                                    label="Start Date"
                                    validation="required"
                                    error-behavior="live"
                                    :disabled="modalReadonly || !formRender.edit.start_date"
                                    ></FormulateInput>
                                <FormulateInput
                                    ref="curriculum-formulate-form-1-end_date"
                                    type="date"
                                    v-model="curriculum.end_date"
                                    label="End Date"
                                    validation="required|later"
                                    
                                    :validation-rules="{
                                        later: () => {
                                            return (
                                                Date.parse(curriculum.start_date) <
                                                Date.parse(curriculum.end_date)
                                            );
                                        },
                                    }"
                                    :validation-messages="{
                                        later: 'End date must be later than start date.',
                                    }"
                                    error-behavior="live"
                                    :disabled="modalReadonly || !formRender.edit.end_date"
                                    ></FormulateInput>
                                <formulate-input ref="curriculum-formulate-form-1-info" label="Info"
                                        :key="'curriculum-formulate-form-1-info-' + formKey" type="textarea"
                                        v-model="curriculum.info" validation="max:200,length"
                                        :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>

                                <div>
                                    <h6>Skillgroups</h6>
                                    <multiselect ref="curriculum-formulate-form-1-skillgroups" name="skillgroups"
                                        v-model="curriculum.skillgroups" v-validate="'required|min:1'"
                                        data-vv-validate-on="input" data-vv-as="skillgroups"  data-vv-scope="curriculum-formulate-form-1"
                                        :hide-selected="true" :close-on-select="false" :multiple="true" :options="skillgroupTable"
                                        :custom-label="_skillgroups_custom_label" track-by="id" placeholder="Select..."
                                        :disabled="modalReadonly || !formRender.edit.skillgroups">
                                    </multiselect>
                                    <span v-show="veeErrors.has('curriculum-formulate-form-1.skillgroups')" style="color: red">{{  veeErrors.first('curriculum-formulate-form-1.skillgroups') }}</span>
                                </div>
                                <p></p>
                                <FormulateInput type="file" ref="curriculum-formulate-form-1-attachment_file"
                                    :key="'curriculum-formulate-form-1-attachment_file-' + formKey"
                                    v-model="curriculum.attachment_file" label="Attachment file"
                                    help="" 
                                    :validation-rules="{ 
                                        maxFileSize :  (context, ... args) => {
                                            if (getFileOrNull(context.value) !== null)
                                                return context.value.files[0].file.size < parseInt(args[0]);
                                            return true;
                                        },
                                        
                                    }"
                                    :validation-messages="{ maxFileSize : (context) => {
                                                return 'The file size must not exceed ' + parseInt(context.args[0]) / (1000000) + ' mb.';},                                     
                                            }" 
                                    error-behavior="live" validation-event="input" validation="optional|maxFileSize:2000000" upload-behavior="delayed" :disabled="
                                        modalReadonly || !formRender.edit.attachment_file
                                    "></FormulateInput>
                                    <button v-if="(copiedCurriculum.attachment_file !== null)" type="button"
                                        class="btn btn-primary" @click="openNewWindow(copiedCurriculum.attachment_file)">
                                        File URL
                                    </button>
                                    <button v-if="(copiedCurriculum.attachment_file !== null)" type="button"
                                        class="btn btn-outline-danger" @click="copiedCurriculum.attachment_file = null; curriculum.attachment_file = ''; formKey += 1;"       
                                        :disabled="modalReadonly">
                                        Remove File
                                    </button>
                                    
                                            
                            </FormulateForm>


                        </div>

                    </div>
                    
                    
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                    </button>
                    <button id="createButton" type="button" @click="createClick()" v-if="addingNewCurriculum && !modalReadonly"
                        class="btn btn-primary">
                        Create
                    </button>

                    <button id="updateButton" type="button" @click="updateClick()" v-if="!addingNewCurriculum && !modalReadonly"
                        class="btn btn-primary">
                        Update
                    </button>
                </div>

            </div >
        </div >
    </div >
    
    <EventAttendanceModal v-model="showCurriculumStudentModal" :click-to-close="false">
        <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
          @click="showCurriculumStudentModal = false" data-bs-toggle="modal" data-bs-target="#edit-info-modal">
          Close
        </button></template>
        <CurriculumStudent v-if="typeof this.testMode === 'undefined'" :curriculum_id="curriculum.id" :user="user"></CurriculumStudent>
    </EventAttendanceModal>

</div >
</template>


<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import * as bootstrap from "bootstrap";
import EventAttendanceModal from "/src/components/event/EventAttendanceModal.vue";
import CurriculumStudent from "/src/components/profile/CurriculumStudent.vue";

export default {
    components: {
        VueGoodTable,
        Multiselect,

        //Custom components
        EventAttendanceModal,
        CurriculumStudent,
    },

    data(){
        return {
            curriculum:{},
            copiedCurriculum:{},
            curriculums:{},

            showCurriculumStudentModal: false,
    
            skillgroupTable:{},

            addingNewCurriculum:false,
            modalTitle:"",
            modalReadonly:false,
            
            variables: {
                API_URL: "",
            },

            formKey:1,
            user:{},
            formRender: {},
            formRenderSpec: {
                staff: {
                    edit: {
                        mode: "exclude",
                        fields: [],
                    },
                },

                student: {
                    edit: {
                        mode: "include",
                        fields: [],
                    },
                },
            },
            
            vgtColumns: [
                {
                    label: "Curriculum ID",
                    field: "id",
                    // tooltip: '',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Thai Name",
                    field: "th_name",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                // {
                //     label: "Academic Year",
                //     field: "start_date",
                //     filterable: true,
                //     type: "date",
                //     dateInputFormat: "yyyy-mm-dd",
                //     dateOutputFormat: "yyyy",
                //     thClass: "text-center",
                //     tdClass: "text-center",
                //     filterOptions: {
                //         enabled: true,
                //         placeholder: "",
                //         // filterFn: this.dateRangeFilter,
                //     },
                // },
                {
                    label: "Start Date",
                    field: "start_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "dd-mm-yyyy",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Start Date",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "End Date",
                    field: "end_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "dd-mm-yyyy",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter End Date",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "Action",
                    field: "action",
                    thClass: "text-center",
                    tdClass: "text-center",
                },
            ],
        }
    },

    methods: {

        getEmptyCurriculum(){
            return {
                id : 0,
                th_name : '',
                en_name : '',
                start_date : '',
                end_date : '',
                info : '',
                attachment_file : null,

                skillgroups : [],
                
            }
        },
        refreshData(){
            axios.get(this.variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });
        },

        async addClick(){
            this.modalTitle="Add Curriculum"
            this.addingNewCurriculum = true // Signal that we are adding a new event -> Create Button.
            this.modalReadonly = false;
            
            await this.assignDataToCurriculumForm(this.getEmptyCurriculum());
            await this.$formulate.resetValidation('curriculum-formulate-form-1')
            this.veeErrors.clear();
        
        },
        viewClick(curriculum){
            this.modalTitle="Edit Curriculum"
            this.addingNewCurriculum = false
            this.modalReadonly = true;

            this.assignDataToCurriculumForm(curriculum);
        },
        editClick(curriculum){
            this.modalTitle="Edit Curriculum"
            this.addingNewCurriculum = false
            this.modalReadonly = false;

            this.assignDataToCurriculumForm(curriculum);
        },
        assignDataToCurriculumForm(curriculum) {
            const stringified = JSON.stringify(curriculum);
            this.curriculum = JSON.parse(stringified);
            this.copiedCurriculum = JSON.parse(stringified);

        },
        
        async createClick(){
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined"){
                return formIsValid;
            }

            if (!formIsValid) return;


            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outForm.append(key.toString(), value)
            }
            outForm.set("skillgroups", JSON.stringify(this.cleanManyToManyFields(this.curriculum.skillgroups)));
            outForm.set("attachment_file", this.cleanAttachmentFile(this.curriculum.attachment_file));

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: this.variables.API_URL+"curriculum",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outForm,
                headers : {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                const data = response.data.data
                const detail = response.data.detail

                this.curriculums.push(data);
                this.editClick(data)
                
                // alert(detail + '\n' + JSON.stringify(data));
                alert(detail);
            }).catch((error)=>{
                alert(error.response.data.detail)
            })

        },

        async updateClick(){
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined"){
                return formIsValid;
            }

            if (!formIsValid) return;

            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outForm.append(key.toString(), value)
            }
            outForm.set("skillgroups", JSON.stringify(this.cleanManyToManyFields(this.curriculum.skillgroups)));
            outForm.set("attachment_file", this.cleanAttachmentFile(this.curriculum.attachment_file));

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: this.variables.API_URL+"curriculum/" + this.curriculum.id,
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outForm,
                headers : {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                const data = response.data.data
                const detail = response.data.detail
                this.reassignUpdatedElementIntoList(this.curriculums, response.data.data);
                this.editClick(data)
                
                // alert(detail + '\n' + JSON.stringify(data) );
                alert(detail);
            }).catch((error)=>{
                alert(error.response.data.detail);
            })
        },

        deleteClick(curriculum_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: this.variables.API_URL+"curriculum/"+ curriculum_id,
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers : {
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.removeElementFromArrayById(this.curriculums, curriculum_id);
                alert(response.data.detail)
            }).catch((error)=>{
                alert(error.response.data.detail);
            });

        },
        removeElementFromArrayById(arr, id){
            for(let i = 0; i < arr.length; ++i){
                if (arr[i].id === id){
                    arr.splice(i, 1);
                    break;
                }
            }
        },
        async validateForm(){
            //Perform validation on the form.
            await this.$formulate.submit("curriculum-formulate-form-1");

            const vue_formulate_valid = this.$refs["curriculum-formulate-form-1"].isValid;
            console.log('vue_formulate_valid', vue_formulate_valid)
            //vee-validate  scope : curriculum
            let vee_validate_valid = false;
            await this.$validator.validateAll("curriculum-formulate-form-1").then((result) => {
                vee_validate_valid = result;
            });
            console.log('vee_validate_valid', vee_validate_valid)
            return vue_formulate_valid && vee_validate_valid;
        },

        onFileSelected(event){
            this.curriculum.attachment_file = event.target.files[0]
        },
        openNewWindow(url){
            window.open(url);
        },
        _generate_formRender() {
            //Generate edit
            const getEmptyObjectFunction = this.getEmptyCurriculum
            // console.log(getEmptyObjectFunction())
            const user = this.user;
            let edit_info = {};

            if (user.is_staff) {
                edit_info = this.formRenderSpec["staff"]["edit"];
            } else if (user.is_student) {
                edit_info = this.formRenderSpec["student"]["edit"];
            }

            const formRender = {};
            formRender["edit"] = {};

            if (edit_info["mode"] === "exclude") {
                Object.entries(getEmptyObjectFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(getEmptyObjectFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },
        _skillgroups_custom_label({ id, name }) {

            const table = this.skillgroupTable;

            if (id === "" || id === null || typeof id === "undefined") {
                return "Select";
            } else if (name === null || typeof name === "undefined") {
                for (let i = 0; i < table.length; ++i) {
                    if (table[i].id === id) {
                        const temp = table[i];
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.name}`;
                    }
                }
            }

            return `${id} ${name}`;
        },
        cleanManyToManyFields(list) {
            //Remove empty or redundant inputs.
            // console.log(list)
            const nonEmpty = [];
            const ids = [];
            for (let i = 0; i < list.length; ++i) {
                const id = list[i]["id"];

                if (id !== "" && !ids.includes(id)) {
                    ids.push(list[i].id);
                    nonEmpty.push({ id: list[i].id });
                }
            }

            return nonEmpty;
        },
        cleanAttachmentFile(attachment_file_field) {
            // Idea : If there is a file, send it. If it is undefined, set it to ''.
            // If it is a file path, we can send it to the backend without any issues.
            const field = attachment_file_field;

            const file = this.getFileOrNull(field);
            if (file instanceof File) return file;
            else {
                if (typeof field === "string")
                    //
                    return field;
            }

            if (typeof field === "undefined") return "";

            return field;
        },
        getFileOrNull(field) {
            //We want to support both file and array of files as a field.

            if (field instanceof File) return field;
            else if (typeof field === "undefined" || field === null) return null;
            else if (typeof field === "string") return null;
            else if (typeof field.files === "undefined" || field.files === null) return null;
            else if (field.files.length === 0) return null;
            else return field.files[0].file;
        },
        dateRangeFilter(data, filterString) {
            const dateRange = filterString.split("to");
            const startDate = Date.parse(dateRange[0]);
            const endDate = Date.parse(dateRange[1]);
            return Date.parse(data) >= startDate && Date.parse(data) <= endDate;
        },
        toggleColumn(index, event) {
            // Set hidden to inverse of what it currently is
            this.$set(
                this.vgtColumns[index],
                "hidden",
                !this.vgtColumns[index].hidden
            );
        },

        reassignUpdatedElementIntoList(list, element) {
            for (let i = 0; i < list.length; ++i) {
                if (list[i].id === element.id) {
                    this.$set(list, i, element);
                    break;
                }
            }
        },
    },

    created: async function(){
        
        if (typeof this.testMode !== 'undefined'){
            this.curriculum = this.getEmptyCurriculum()
            this._generate_formRender()
            return;
        }


        this.curriculum = this.getEmptyCurriculum()
        this.variables.API_URL = this.$API_URL
        await axios.get(this.$API_URL + "user")
            .then((response) => {
                this.user = response.data;
                
            })

        this._generate_formRender()

        axios.get(this.variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });
        
        axios.get(this.variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillgroupTable=response.data;
            });

        this.$nextTick(() => {

                document.getElementById('edit-info-modal').addEventListener("hidden.bs.modal", (event) => {
                    this.veeErrors.clear();
                    this.formKey += 1;
                });

                const inputs = [
                    // 'input[placeholder="Filter Received"]',
                    'input[placeholder="Filter Start Date"]',
                    'input[placeholder="Filter End Date"]',
                ];

                inputs.forEach(function (input) {
                    flatpickr(input, {
                        dateFormat: "d-m-Y",
                        mode: "range",
                        allowInput: true,
                        // enableTime:true,
                    });
                });
            });

    },

    mounted: function(){


    },
    
}

</script>