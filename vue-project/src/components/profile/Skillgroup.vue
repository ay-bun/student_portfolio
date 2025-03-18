<template>
    <div>
        <h1 class="text-center">ระบบการจัดการกลุ่มของทักษะ</h1>
        
        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
            Add Skillgroup
        </button>

        <vue-good-table ref="skillgroup-vgt" :columns="vgtColumns" :rows="skillgroups"
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
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="index" href="#">
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
                <span v-if="props.column.field == 'action'">
                    <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1" data-bs-toggle="modal"
                        data-bs-target="#edit-info-modal" @click="viewClick(props.row)">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button v-if="user.is_staff" type="button" :id="'edit-button-' + props.row.id"
                        class="btn btn-light mr-1" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
                        @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="user.is_staff" type="button" @click="deleteClick(props.row.id)"
                        class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>
        <div class="modal fade" id="edit-info-modal" tabindex="-1" aria-labelledby="edit-info-modal-label"
            aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="edit-info-modal-label">
                            {{ modalTitle }}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">
                                <FormulateForm name="skillgroup-formulate-form-1" ref="skillgroup-formulate-form-1">
                                    <formulate-input ref="skillgroup-formulate-form-1-name" type="text"
                                        v-model="skillgroup.name" label="Name" validation="required|max:50"
                                        :readonly="modalReadonly || !formRender.edit.name"></formulate-input>
                                    <formulate-input ref="skillgroup-formulate-form-1-info" label="Info"
                                        :key="'skillgroup-formulate-form-1-info' + formKey" type="textarea"
                                        v-model="skillgroup.info" validation="max:200,length"
                                        :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>
                                        <FormulateInput
                                            ref="skillgroup-formulate-form-1-skills"
                                            v-model="skillgroup.skills"
                                            type="group"
                                            name="skills"
                                            :key="'skillgroup-formulate-form-1' + '-group-' + formKey"
                                            :repeatable="!modalReadonly"
                                            label="Skills"
                                            add-label="+ Add Skill"
                                            validation="required"
                                        >                        
                                            <FormulateInput type="vue-select" name="skill_id_fk" validation-name="Skill" label="Skill" :options="skillTableVueSelect" :disabled="modalReadonly || !formRender.edit.skills"></FormulateInput>
                                            <FormulateInput type="number" name='goal_point' validation-name="Goal Point" label="Goal Point" validation="required|min:0|max:10" :disabled="modalReadonly || !formRender.edit.skills"></FormulateInput> 
                                            
                                        </FormulateInput>
                                </FormulateForm>


                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                            <button id="createButton" type="button" @click="createClick()" v-if="addingNewSkillgroup && !modalReadonly"
                                class="btn btn-primary">
                                Create
                            </button>

                            <button id="updateButton" type="button" @click="updateClick()" v-if="!addingNewSkillgroup && !modalReadonly"
                                class="btn btn-primary">
                                Update
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import * as bootstrap from "bootstrap";

export default {
    components: {
        VueGoodTable,
        Multiselect,
    },

    data() {
        return {
            skillgroup: {},
            copiedSkillgroup: {},
            skillgroups: [],

            // inputGroup : [],

            skillTableVueSelect : [],
            skillTable: [],

            user: {},
            addingNewSkillgroup: false,
            formKey: 1,
            variables: {
                API_URL: "",
            },

            modalTitle: "",
            modalReadonly: false,
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
                    label: "Skillgroup ID",
                    field: "id",
                    // tooltip: '',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter ID", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Name",
                    field: "name",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter Name", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Action",
                    field: "action",
                    thClass: "text-center",
                    tdClass: "text-center",
                },
            ],
        };
    },

    methods: {
        getEmptySkillgroup() {
            return {
                id: 0,
                name: "",
                info: "",
                skills: "",
            };
        },

        refreshData() {
            axios.get(this.variables.API_URL + "skillgroup").then((response) => {
                this.skillgroups = response.data;
            });
        },

        addClick() {
            this.modalTitle = "Add Skillgroup";
            this.addingNewSkillgroup = true; // Signal that we are adding a new event -> Create Button.
            this.modalReadonly = false;

            this.assignDataToSkillgroupForm(this.getEmptySkillgroup());
        },
        viewClick(skillgroup) {
            this.modalTitle = "View Skillgroup";
            this.addingNewSkillgroup = false;
            this.modalReadonly = true;

            // this.formKey += 1
            
            this.assignDataToSkillgroupForm(skillgroup);
        },
        editClick(skillgroup) {
            this.modalTitle = "Edit Skillgroup";
            this.addingNewSkillgroup = false;
            this.modalReadonly = false;

            this.assignDataToSkillgroupForm(skillgroup);
        },
        assignDataToSkillgroupForm(formData) {
            const stringified = JSON.stringify(formData);
            this.skillgroup = JSON.parse(stringified);
            this.copiedSkillgroup = JSON.parse(stringified);

            this.skillgroup.skills = this.convertFieldToString(this.skillgroup.skills, 'skill_id_fk')
            this.copiedSkillgroup.skills = this.convertFieldToString(this.copiedSkillgroup.skills, 'skill_id_fk')

        },
        async createClick() {
            this.skillgroup.skills = this.cleanManyToManyFieldsWithFieldSelection(this.skillgroup.skills, 'skill_id_fk', ['goal_point']);

            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined"){
                return formIsValid
            }

            if (!formIsValid) return;

            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outForm.append(key.toString(), value);
            }
            outForm.set("skills", JSON.stringify(this.skillgroup.skills));
            
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.variables.API_URL + "skillgroup",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                const data = response.data.data
                const detail = response.data.detail
                this.skillgroups.push(data);
                this.editClick(data)//Change viewing mode.
                
                // alert(detail + '\n' + JSON.stringify(data));
                alert(detail);
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },
        
        async updateClick() {

            this.skillgroup.skills = this.cleanManyToManyFieldsWithFieldSelection(this.skillgroup.skills, 'skill_id_fk', ['goal_point']);

            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });
            
            if (typeof this.testMode !== "undefined"){
                return formIsValid
            }
            
            if (!formIsValid) return;

            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outForm.append(key.toString(), value);
            }
            outForm.set("skills", JSON.stringify(this.skillgroup.skills));
               
            //Make a request.
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.variables.API_URL + "skillgroup/" + this.skillgroup.id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                let data = response.data.data
                data.skills = this.convertFieldToString(data.skills, 'skill_id_fk')
                const detail = response.data.detail
                this.reassignUpdatedElementIntoList(this.skillgroups, data); //With reactivity.
                this.editClick(data)
                // alert(detail + '\n' + JSON.stringify(data) );
                alert(detail);
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },

        deleteClick(skillgroup_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url: this.variables.API_URL + "skillgroup/" + skillgroup_id,
                xstfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.removeElementFromArrayById(this.skillgroups, skillgroup_id);
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
        reassignUpdatedElementIntoList(list, element) {
            for (let i = 0; i < list.length; ++i) {
                if (list[i].id === element.id) {
                    this.$set(list, i, element);
                    break;
                }
            }
        },
        convertFieldToString(list, fieldName){
            for(let i=0; i < list.length; ++i){
                list[i][fieldName] = String(list[i][fieldName])
            }
            return list
        },
        cleanManyToManyFieldsWithFieldSelection(list, distintFieldName="id", selectedFields=[]) {
            //Remove empty or redundant inputs.
            
            // id (distintFieldName) is selected by default.

            const nonEmpty = [];
            const ids = [];
            for (let i = 0; i < list.length; ++i) {
                let element = list[i]
                const elemnt_id = element[distintFieldName];

                if (!ids.includes(elemnt_id) && elemnt_id !== "" && elemnt_id !== null && typeof elemnt_id !== 'undefined' ) {
                    ids.push(elemnt_id);
                    
                    let tempDict = {}
                    tempDict[distintFieldName] = elemnt_id
                    selectedFields.forEach((fieldName)=>{
                        tempDict[fieldName] = element[fieldName]
                    })

                    nonEmpty.push(tempDict);
                }
            }
            
            return nonEmpty;
        },

        async validateForm() {
            await this.$formulate.submit("skillgroup-formulate-form-1");

            const vue_formulate_valid =
                this.$refs["skillgroup-formulate-form-1"].isValid;

            // //vee-validate :validate the scope : skillgroup
            // let vee_validate_valid = false;
            // await this.$validator.validateAll("skillgroup").then((result) => {
            //     vee_validate_valid = result;
            // });

            return vue_formulate_valid;
        },
        _generate_formRender() {
            //Generate edit
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
                Object.entries(this.getEmptySkillgroup()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(this.getEmptySkillgroup()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },
        _skills_custom_label({ skill_id_fk, title }) {
            let id = skill_id_fk;
            if (id === "" || id === null || typeof id === "undefined") {
                return "Select";
            } else if (title === null || typeof title === "undefined") {
                for (let i = 0; i < this.skillTable.length; ++i) {
                    if (this.skillTable[i].id === id) {
                        const temp = this.skillTable[i];
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.title}`;
                    }
                }
            }

            return `${id} ${title}`;
        },

        _generate_skillTableVueSelect(){
            let arr = []
            this.skillTable.forEach((element)=>{
                arr.push({'value' : `${element.id}`, 'label' : `${element.id} ${element.title}`})
            })
            // console.log(arr)
            this.skillTableVueSelect = arr
        },
        
        dateRangeFilter(data, filterString) {
            const dateRange = filterString.split("to");
            const startDate = Date.parse(dateRange[0]);
            const endDate = Date.parse(dateRange[1]);
            return Date.parse(data) >= startDate && Date.parse(data) <= endDate;
        },
        _data_processing_for_test(){
            this.skillgroup = this.getEmptySkillgroup()
            this._generate_formRender();
            this._generate_skillTableVueSelect(); //vue-formulte select needs to work with ids as strings.

        },
    },
    created: async function () {
        if (typeof this.testMode !== "undefined") {
           this._data_processing_for_test()
            return;
        }

        this.skillgroup = this.getEmptySkillgroup();
        this.variables.API_URL = this.$API_URL
        await axios.get(this.variables.API_URL + "user").then((response) => {
            this.user = response.data;
            this._generate_formRender(); //Generate the form rendering rule based on user.
        });

        axios.get(this.variables.API_URL + "skillgroup").then((response) => {
            this.skillgroups = response.data;       
        });

        axios.get(this.variables.API_URL + "skillTable").then((response) => {
            this.skillTable = response.data;
            this._generate_skillTableVueSelect();
            // console.log(this.)
        });

        this.$nextTick(() => {
            document
                .getElementById("edit-info-modal")
                .addEventListener("hidden.bs.modal", (event) => {
                    this.veeErrors.clear();
                    this.formKey += 1;
                });

            })
    },

    mounted: function () {

    },
};
</script>
