<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

// import flatpickr from 'flatpickr'
// import 'flatpickr/dist/flatpickr.min.css'
import * as bootstrap from "bootstrap";

// import { $vfm, VueFinalModal, ModalsContainer } from "vue-final-modal";

// import AttendanceModal from "/src/components/event/AttendanceModal.vue"
import AddAttendanceModal from "/src/components/event/AddAttendanceModal.vue";

export default {
    components: {
        VueGoodTable,
        Multiselect,
        // VueFinalModal,

        AddAttendanceModal,
    },

    props: {
        event_id : {
            type: Number,
            default : 0,
        },
        user :{
            type: Object,
            required : true,
            default : null,
        }
    },

    data() {
        return {
            // user:{},
            modalTitle: "",
            addingNewAttendance: false,
            
            rowActionChexboxes: [],
            showRowActionEditUsedForCalculationModal:false,

            multiselect: {
                // student : {university_id:''}, //multiselect will treat this as a dict.
                student: "",
            },

            formKey: 1,
            eventAttendance: {},
            eventAttendances: [],
            modalReadonly: false,
            
            studentTable: [],
            
            showAddEventAttendanceModal: false,
            showAddByFileModal: false,

            addByFileForm: {
                csvFile: "",
                all_must_valid: true,
                all_passed : false,
                checkboxes: ["all_must_valid"],
                
                //Do not need reset
                checkboxFields: ["all_must_valid", "all_passed"],
                formKey: 1,
            },
            
            checkboxes: [],
            checkboxFields: ["used_for_calculation"],
            formRender :{},
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
                    label: "Attendance Id",
                    field: "id",
                    // tooltip: 'A simple tooltip',
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
                    label: "University Id",
                    field: "university_id",
                    // tooltip: 'A simple tooltip',
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
                    label: "Firstname",
                    field: "firstname",
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
                {
                    label: "Lastname",
                    field: "lastname",
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
                {
                    label: "Synced",
                    field: "synced",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip : "รหัสนักศึกษาอยู่ในฐานข้อมูล",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "All", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [true, false], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnApprovedFilterFn, //custom filter function that
                        trigger: "enter", //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Passed",
                    field: "used_for_calculation",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip : "ผ่านการทดสอบ (used_for_calculation)",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "All", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [true, false], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnApprovedFilterFn, //custom filter function that
                        trigger: "enter", //only trigger on enter not on keyup
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
        getEmptyEventAttendance() {
            return {
                id: 0,
                event_id_fk: "",
                university_id: null,

                firstname: "",
                middlename: "",
                lastname: "",

                user_id_fk: "",
                synced: false,

                used_for_calculation: false,
            };
        },

        refreshData() {
            axios
                .get(this.$API_URL + "event-attendance/" + this.event_id)
                .then((response) => {
                    this.eventAttendances = response.data;
                    // console.log(this.eventAttendances)
                });
        },
        addClick() {
            this.modalTitle = "Add Student";
            this.addingNewAttendance = true; // Signal that we are adding a new student -> Create Button.
            this.modalReadonly = false;

            this.assignDataToEventAttendanceForm(this.getEmptyEventAttendance())
        },
        viewClick(attendance) {
            this.modalTitle = "View Mode";
            this.addingNewAttendance = false;
            this.modalReadonly = true;
            
            this.assignDataToEventAttendanceForm(attendance)
        },    
        editClick(attendance) {
            this.modalTitle = "Edit Event Attedance";
            this.addingNewAttendance = false;
            this.modalReadonly = false;

            this.assignDataToEventAttendanceForm(attendance)
        },
        assignDataToEventAttendanceForm(attendance) {

            const stringified = JSON.stringify(attendance);
            this.eventAttendance = JSON.parse(stringified);
            this.eventAttendance.university_id = { university_id: attendance.university_id };

            this.checkboxes = this.getListOfTrueCheckboxFields(this.eventAttendance, this.checkboxFields);
        },
        getListOfTrueCheckboxFields(formdata, checkboxFields) {
            const checkboxes = [];
            for (let i = 0; i < checkboxFields.length; ++i) {
                if (formdata[checkboxFields[i]] === true)
                    checkboxes.push(checkboxFields[i]);
            }
            return checkboxes;
        },
        assignBooleanValueToCheckboxFields(formdata, checkboxes, checkboxFields) {
            for (let i = 0; i < checkboxFields.length; ++i) {
                const field_name = checkboxFields[i];
                formdata[field_name] = checkboxes.includes(field_name);
            }
        },
        async createClick() {
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined"){
                return formIsValid;
            }
                
            if (!formIsValid) return;
            
            this.assignBooleanValueToCheckboxFields(this.eventAttendance, this.checkboxes, this.checkboxFields)

            // this.eventAttendance.university_id = this.multiselect.student.university_id;
                
            const outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value);
            }
            outDict.set("event_id_fk", this.event_id);
            outDict.set('university_id', this.eventAttendance.university_id.university_id)
            
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "event-attendance/",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                const data = response.data.data
                const detail = response.data.detail
                this.eventAttendances.push(data);
                this.editClick(data) //Change viewing mode.
                // alert(detail + '\n' + JSON.stringify(data));
                alert(detail);
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },
        async updateClick() {

            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined"){
                return formIsValid;
            }
                
            if (!formIsValid) return;

            this.assignBooleanValueToCheckboxFields(this.eventAttendance, this.checkboxes, this.checkboxFields)

            // this.eventAttendance.university_id = this.multiselect.student.university_id;
                
            // console.log(this.eventAttendance);
            const outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value);
            }
            outDict.set('university_id', this.eventAttendance.university_id.university_id)
            
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url:
                    this.$API_URL +
                    "event-attendance/" +
                    this.event_id +
                    "/" +
                    this.eventAttendance.id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                const data = response.data.data
                const detail = response.data.detail
                this.reassignUpdatedElementIntoList(this.eventAttendances, data); //With reactivity.
                this.editClick(data)

                alert(detail + '\n' + JSON.stringify(data) );
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },

        deleteClick(attendance_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url:
                    this.$API_URL +
                    "event-attendance/" +
                    this.event_id +
                    "/" +
                    attendance_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.removeElementFromArrayById(this.eventAttendances, attendance_id);
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
        async validateForm() {
            //Perform validation on the form.
            const formulate_form_formname = "event-attendance-formulate-form-1"
            await this.$formulate.submit(formulate_form_formname);

            const vue_formulate_valid = this.$refs[formulate_form_formname].isValid;
            console.log('vue_formulate_valid', vue_formulate_valid)
            //vee-validate scope : formulate_form_formname
            let vee_validate_valid = false;
            await this.$validator.validateAll(formulate_form_formname).then((result) => {
                vee_validate_valid = result;
            });
            console.log('vee_validate_valid', vee_validate_valid)
            return vue_formulate_valid && vee_validate_valid;
        },
        syncByUniversityIdClick() {
            const outDict = {
                event_id: this.event_id,
            };

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url:
                    this.$API_URL + "sync-attendance-by-university-id/" + this.event_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        onCSVFileSelected(event) {
            this.csv_file = event.target.files[0];
        },
        async bulkAddClick() {
            let formIsValid = false;
            await this.validateAddByFileForm().then((result) => {
                formIsValid = result;
            });

            if (!formIsValid) return;

            const form = this.addByFileForm;
            for (let i = 0; i < form.checkboxFields.length; ++i) {
                const fieldName = form.checkboxFields[i];
                form[fieldName] = form.checkboxes.includes(fieldName);
            }

            const outDict = {
                event_id: this.event_id,
                csv_file: this.cleanAttachmentFile(form.csvFile),
                all_must_valid: form.all_must_valid,
                all_passed : form.all_passed,
            };
            // console.log(outDict);
            const outForm = new FormData();
            for (const [key, value] of Object.entries(outDict)) {
                outForm.append(key.toString(), value);
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "event-attendance-bulk-add",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            })
                .then((response) => {
                    this.refreshData();
                    alert(response.data.detail);

                    if (typeof response.data.invalid_rows !== 'undefined')
                        alert(response.data.invalid_rows );
                })
                .catch((error) => {
                    alert(error.response.data.detail );
                    if (typeof error.response.data.invalid_rows !== 'undefined')
                        alert(error.response.data.invalid_rows );
                    
                    if (typeof error.response.data.serializer_errors !== 'undefined')
                        console.log(error.response.data.serializer_errors)

                });
        },
        _university_id_custome_label({ university_id, firstname, lastname }) {
            if (
                university_id === "" ||
                Object.is(university_id, null) ||
                typeof university_id === "undefined"
            )
                return "select...";
            else {
                for (let i = 0; i < this.studentTable.length; ++i) {
                    if (this.studentTable[i].university_id === university_id) {
                        const temp = this.studentTable[i];
                        return `${temp.university_id} ${temp.firstname} ${temp.lastname}`;
                    }
                }
                //Not Found
                return "select...";
            }
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
        async validateAddByFileForm() {
            await this.$formulate.submit("event-attendance-formulate-form-2");

            const vue_formulate_valid =
                this.$refs["event-attendance-formulate-form-2"].isValid;

            return vue_formulate_valid;
        },

        _on_add_attendance_modal_closed() {
            this.eventAttendance = this.getEmptyEventAttendance();
        },
        _on_add_by_file_modal_closed() {
            this.addByFileForm.formKey += 1;

            this.addByFileForm.csvFile = "";
            this.addByFileForm.all_must_valid = true;
            this.addByFileForm.all_passed = false;
            this.addByFileForm.checkboxes = ["all_must_valid"];
        },
        toggleColumn(index, event) {
            // Set hidden to inverse of what it currently is
            this.$set(
                this.vgtColumns[index],
                "hidden",
                !this.vgtColumns[index].hidden
            );
        },
        _generate_formRender() {
            //Generate edit
            // console.log('In generate form render')
            // console.log(this.user)
            const user = this.user;
            let getEmptyObjectFunction = this.getEmptyEventAttendance

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

        rowActionEditUsedForCalculation(){
            const selectedRows = this.$refs['event-attendance-vgt'].selectedRows;
            
            const ids = [];
            for (let i = 0; i < selectedRows.length; ++i) {
                ids.push(selectedRows[i].id);
            }
            const outForm = new FormData();
            outForm.append("ids", JSON.stringify(ids));
            outForm.append("used_for_calculation", (this.rowActionChexboxes === 'passed'))

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.$API_URL + "event-attendance/multi-edit-used_for_calculation",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                // this.refreshData();
                let bool_val = (this.rowActionChexboxes === 'passed');
                for (let i = 0; i < selectedRows.length; ++i) {
                    // selectedRows[i].used_for_calculation
                    this.$set(selectedRows[i], 'used_for_calculation', bool_val)
                }
                alert(response.data.detail)
                this.showRowActionEditUsedForCalculationModal = false;          
            }).catch((error) => {
                alert(error.response.data.detail);
                this.showRowActionEditUsedForCalculationModal = false;
            })

        }
    },

    watch: {
        event_id: function (new_event_id, old_event_id) {

            if (new_event_id !== 0){
                this.refreshData();
            }
                
        },
        user: function(new_user, old_user){
            if (new_user !== null){
                this._generate_formRender();
            }
        }
    },

    created: function () {
        
        if (typeof this.testMode !== 'undefined'){
            if (this.user !== null){
                this._generate_formRender();
            }
            return;
        }

        axios.get(this.$API_URL + "student").then((response) => {
            this.studentTable = response.data;
        });

        if (this.user !== null){
            this._generate_formRender();
        }
        // console.log(this.user) user is passed via props.
        
    },
    mounted: function () {
        // this.event_id = JSON.parse(document.getElementById('event_id-data').textContent);
        // console.log(this.event_id)
        // this.refreshData()
    },
};
</script>

<template>
    <div>
        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="
            addClick();
        showAddEventAttendanceModal = true;
                  ">
            Add Student to The Event
        </button>

        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="syncByUniversityIdClick()">
            Sync by university id
        </button>
        
        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="showAddByFileModal = true">
            Add attendees by file
        </button>

        <vue-good-table ref="event-attendance-vgt" :columns="vgtColumns" :rows="eventAttendances"
            :select-options="{ enabled: user.is_staff, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 20,
                setCurrentPage: 1,
            }">
            <div slot="selected-row-actions">
                <button @click="showRowActionEditUsedForCalculationModal=true; rowActionChexboxes = 'passed';">Set Used for Calculation</button>
            </div>
            <div slot="table-actions">
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        columns
                    </button>

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="column.label + '--'+index" href="#">
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
                    <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1"
                            @click="viewClick(props.row); showAddEventAttendanceModal = true">
                            <i class="bi bi-eye"></i>
                    </button>
                    
                    <button v-if="user.is_staff" type="button" :id="'edit-button-' + props.row.id"
                        class="btn btn-light mr-1" @click="
                            editClick(props.row);
                        showAddEventAttendanceModal = true;
                                        ">
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

        <AddAttendanceModal v-model="showAddEventAttendanceModal" :click-to-close="false" :hide-overlay="false"
            :lock-scroll="true" @closed="_on_add_attendance_modal_closed()">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showAddEventAttendanceModal = false">
                    Close
                </button></template>
            <FormulateForm name="event-attendance-formulate-form-1" ref="event-attendance-formulate-form-1"
                >
                <h6>University Id</h6>
                <div class="multiselect-university_id">
                    <!-- v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="receivers" -->
                    <multiselect ref="event-attendance-formulate-form-1-university_id"
                        name="university_id" v-model="eventAttendance.university_id"
                        v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="university id" data-vv-scope="event-attendance-formulate-form-1"
                        :hide-selected="true" :close-on-select="false" :multiple="false" :options="studentTable"
                        :custom-label="_university_id_custome_label" track-by="university_id" placeholder="Select..."
                        :disabled="modalReadonly || !formRender.edit.university_id">
                    </multiselect>
                    <span v-show="veeErrors.has('event-attendance-formulate-form-1.university_id')"
                        class="formulate-input-errors" style="color: red">{{
                            veeErrors.first("event-attendance-formulate-form-1.university_id")
                        }}</span>
                </div>
                
                <formulate-input label="Firstname" ref="event-attendance-formulate-form-1-firstname" type="text"
                    v-model="eventAttendance.firstname" validation="max:50" :readonly="modalReadonly || !formRender.edit.firstname"></formulate-input>
                <formulate-input label="Middlename" ref="event-attendance-formulate-form-1-middlename" type="text"
                    v-model="eventAttendance.middlename" validation="max:50" :readonly="modalReadonly || !formRender.edit.middlename"></formulate-input>
                <formulate-input label="Lastname" ref="event-attendance-formulate-form-1-lastname" type="text"
                    v-model="eventAttendance.lastname" validation="max:50" :readonly="modalReadonly || !formRender.edit.lastname"></formulate-input>
                <formulate-input ref="event-attendance-formulate-form-1-used_for_calculation" type="checkbox"
                    v-model="checkboxes" :options="{ used_for_calculation: 'Use for calculation' }" validation=""
                    :disabled="modalReadonly || !formRender.edit.used_for_calculation"></formulate-input>
            </FormulateForm>
            <button type="button" @click="createClick()" v-if="addingNewAttendance && user.is_staff" class="btn btn-primary">
                Create
            </button>
            <button type="button" @click="updateClick()" v-if="!addingNewAttendance && !modalReadonly && user.is_staff" class="btn btn-primary">
                Update
            </button>
        </AddAttendanceModal>

        <AddAttendanceModal v-model="showAddByFileModal" :click-to-close="false" @closed="_on_add_by_file_modal_closed">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showAddByFileModal = false">
                    Close
                </button></template>
            <FormulateForm name="event-attendance-formulate-form-2" ref="event-attendance-formulate-form-2">
                <FormulateInput type="file" :key="
                    'event-attendance-formulate-form-2-attachment_file-' +
                    addByFileForm.formKey
                " ref="event-attendance-formulate-form-2-attachment_file"
                    v-model="addByFileForm.csvFile"
                    label="Attachment file" help="" 
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
                    error-behavior="live" validation-event="input" validation="required|maxFileSize:2000000|mime:text/csv" upload-behavior="delayed"
                    :disabled="false">
                </FormulateInput>
                <FormulateInput ref="event-attendance-formulate-form-2-all-valid-checkbox"
                    v-model="addByFileForm.checkboxes" :options="{ all_must_valid: 'All rows must be valid.' }"
                    type="checkbox" :disabled="false">
                </FormulateInput>
                <FormulateInput ref="event-attendance-formulate-form-2-all-passed-checkbox"
                    v-model="addByFileForm.checkboxes" :options="{ all_passed: 'All passed.' }"
                    type="checkbox" :disabled="false">
                </FormulateInput>
                <button type="button" @click="bulkAddClick()" class="btn btn-primary">
                    Process
                </button>
            </FormulateForm>
        </AddAttendanceModal>

        <AddAttendanceModal v-model="showRowActionEditUsedForCalculationModal" :click-to-close="false" @closed="rowActionChexboxes = '';">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showRowActionEditUsedForCalculationModal = false">
                    Close
                </button></template>
            <FormulateForm>
                
                <FormulateInput
                    v-model="rowActionChexboxes" :options="{ passed : 'Passed', failed : 'Failed' }"
                    type="radio" :disabled="false">
                </FormulateInput>

                <button type="button" @click="rowActionEditUsedForCalculation();" class="btn btn-primary">
                    Update
                </button>
            </FormulateForm>
        </AddAttendanceModal>
    </div>
</template>

<style scoped>
.multiselect-university_id {
    width: 68%;
}

.formulate-form {
    width: 50%;
}
</style>
