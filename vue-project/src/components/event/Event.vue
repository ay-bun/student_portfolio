<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";

import * as bootstrap from "bootstrap"; //where is bootstrap-icons??
import "vue-datetime/dist/vue-datetime.min.css";

// import { $vfm, VueFinalModal, ModalsContainer } from "vue-final-modal";

// components
import EventAttendance from "/src/components/event/EventAttendance.vue";
import EventAttendanceModal from "/src/components/event/EventAttendanceModal.vue";

export default {
    components: {
        VueGoodTable,
        Multiselect,

        // VueFinalModal,

        //Custom components
        EventAttendanceModal,
        EventAttendance,
    },
    props: {
        onlyAttendedByUser: {
            type: Boolean,
            default: false,
        },
    },
    watch: {

    },
    data() {
        return {
            events: [],
            user: null,

            modalTitle: "",
            addingNewEvent: false,
            showApproved: true,
            modalReadonly: false,

            showEventAttendanceModal: false,
            queryParameters: {
                lower_bound_start_datetime: "2024-01-01T00:00:00.000Z",
                upper_bound_start_datetime: "2028-12-01T00:00:00.000Z",

            },

            asyncSeachEventVariables: {
                event_search_term: '',
                isLoading: false,
                event: null,
                events: [],
            },

            event: {},
            copiedEvent: {},

            skillTable: [],
            staffTable: [],
            checkboxes: [],
            checkboxFields: ["approved", "used_for_calculation", "arranged_inside"],

            formKey: 1,
            // testMode: false,

            formRenderSpec: {
                staff: {
                    edit: {
                        mode: "exclude",
                        fields: [],
                    },
                },

                student: {
                    edit: {
                        mode: "exclude",
                        fields: ["used_for_calculation", "approved"],
                    },
                },
            },

            formRender: {},
            vgtColumns: [
                {
                    label: "Event ID",
                    field: "id",
                    // tooltip: "A simple tooltip",
                    thClass: "text-center",
                    tdClass: "text-center",
                    hidden: false,
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
                    label: "Title",
                    field: "title",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip: "ชื่อกิจกรรม",
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
                    label: "Start",
                    field: "start_datetime",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-MM-dd'T'HH:mm",
                    dateOutputFormat: "dd-MM-yyyy HH:mm",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip: "วันที่และเวลาที่เริ่มกิจกรรม",
                    filterOptions: {
                        enabled: false,
                        placeholder: "Filter Start",
                        filterFn: this.datetimeRangeFilter,
                    },
                },
                {
                    label: "End",
                    field: "end_datetime",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-MM-dd'T'HH:mm",
                    dateOutputFormat: "dd-MM-yyyy HH:mm",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip: "วันที่และเวลาที่สิ้นสุดการจัดกิจกรรม",
                    filterOptions: {
                        enabled: false,
                        placeholder: "Filter Start",
                        filterFn: this.datetimeRangeFilter,
                    },
                },
                {
                    label: "Approved",
                    field: "approved",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip: "ผ่านการอนุมัติ",
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
                    label: "Arranged Inside",
                    field: "arranged_inside",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip: "จัดโดยวิทยาลัยการคอมพิวเตอร์",
                    hidden: true,
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
        getEmptyEvent() {
            return {
                id: 0,
                title: "",
                start_datetime: '',
                end_datetime: '',
                info: "",

                created_by: "",
                approved: false,
                approved_by: "",
                used_for_calculation: false,
                arranged_inside: false,
                attachment_link: "",
                attachment_file: null,

                //Additional data.
                skills: [],
                staffs: [],
            };
        },

        refreshData() {

            if (this.onlyAttendedByUser) {
                const eventAttendedParams = new URLSearchParams([]);
                axios.get(this.$API_URL + "event-attended/list", { params: eventAttendedParams })
                    .then((response) => {
                        this.events = response.data;
                        // console.log(this.events)
                    });
            }
            else {
                // console.log(this.queryParameters)
                const searchParams = new URLSearchParams([['lower_bound_start_datetime', this.queryParameters.lower_bound_start_datetime],
                ['upper_bound_start_datetime', this.queryParameters.upper_bound_start_datetime]]);
                axios.get(this.$API_URL + "event", { params: searchParams }).then((response) => {
                    this.events = response.data;
                });
            }

        },
        addClick() {
            this.modalTitle = "Add Event";
            this.addingNewEvent = true;
            this.modalReadonly = false;

            this.assignDataToEventForm(this.getEmptyEvent());
        },

        viewClick(event) {
            this.modalTitle = "Event (read only mode)";
            this.addingNewEvent = false;
            this.modalReadonly = true;

            this.assignDataToEventForm(event);
        },

        editClick(event) {
            this.modalTitle = "Edit Event";
            this.addingNewEvent = false;
            this.modalReadonly = false;

            this.assignDataToEventForm(event);
        },
        assignDataToEventForm(event) {
            const stringified = JSON.stringify(event);
            this.event = JSON.parse(stringified);
            this.copiedEvent = JSON.parse(stringified);

            this.checkboxes = this.getListOfTrueCheckboxFields(
                event,
                this.checkboxFields
            );
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

            if (typeof this.testMode !== "undefined") {
                return formIsValid;
            }

            if (!formIsValid) return;
            //Packing values.
            this.assignBooleanValueToCheckboxFields(
                this.event,
                this.checkboxes,
                this.checkboxFields
            );
            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outForm.append(key.toString(), value);
            }
            outForm.set(
                "attachment_file",
                this.cleanAttachmentFile(this.event.attachment_file)
            );
            outForm.set(
                "skills",
                JSON.stringify(this.cleanManyToManyFields(this.event.skills))
            );
            outForm.set(
                "staffs",
                JSON.stringify(this.cleanManyToManyFields(this.event.staffs))
            );

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "event",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            })
                .then((response) => {
                    const data = response.data.data
                    const detail = response.data.detail
                    this.events.push(data);
                    this.editClick(data) //Change viewing mode.
                    // alert(detail + '\n' + JSON.stringify(data));
                    alert(detail + '\n');
                })
                .catch((error) => {
                    alert(error.response.data.detail);
                });
        },

        async updateClick() {

            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof this.testMode !== "undefined") {

                return formIsValid;
            }

            if (!formIsValid) return;

            this.assignBooleanValueToCheckboxFields(
                this.event,
                this.checkboxes,
                this.checkboxFields
            );
            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outForm.append(key.toString(), value);
            }
            outForm.set(
                "attachment_file",
                this.cleanAttachmentFile(this.event.attachment_file)
            );
            outForm.set(
                "skills",
                JSON.stringify(this.cleanManyToManyFields(this.event.skills))
            );
            outForm.set(
                "staffs",
                JSON.stringify(this.cleanManyToManyFields(this.event.staffs))
            );

            //Make a request.
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.$API_URL + "event/" + this.event.id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            })
                .then((response) => {
                    const data = response.data.data
                    const detail = response.data.detail
                    this.reassignUpdatedElementIntoList(this.events, data);
                    this.editClick(data)
                    // alert(detail + '\n' + JSON.stringify(data));
                    alert(detail + '\n');
                })
                .catch((error) => {
                    alert(error.response.data.detail);
                });
        },

        deleteClick(event_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url: this.$API_URL + "event/" + event_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.removeElementFromArrayById(this.events, event_id);
                alert(response.data.detail);
            }).catch((error) => {
                alert(error.response.data.detail);
            })
        },
        removeElementFromArrayById(arr, id) {

            for (let i = 0; i < arr.length; ++i) {
                if (arr[i].id === id) {
                    arr.splice(i, 1);
                    break;
                }
            }
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

        reassignUpdatedElementIntoList(list, element) {
            // console.log(list)
            // console.log(element)
            for (let i = 0; i < list.length; ++i) {
                if (list[i].id === element.id) {
                    this.$set(list, i, element);
                    break;
                }
            }
        },

        openNewWindow(url) {
            window.open(url);
        },

        _skills_custom_label({ id, title }) {
            if (id === "" || id === null || typeof id === 'undefined') {
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

        _staffs_custom_label({ id, university_id, firstname, lastname }) {
            if (id === "" || Object.is(id, null)) {
                return "Select";
            } else if (university_id == null) {
                for (let i = 0; i < this.staffTable.length; ++i) {
                    if (this.staffTable[i].id === id) {
                        const temp = this.staffTable[i];
                        return `${temp.firstname} ${temp.lastname}`;
                    }
                }
            }

            return `${firstname} ${lastname}`;
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

        toggleColumn(index, event) {
            // Set hidden to inverse of what it currently is
            this.$set(
                this.vgtColumns[index],
                "hidden",
                !this.vgtColumns[index].hidden
            );
        },

        datetimeRangeFilter(data, filterString) {
            const dateRange = filterString.split("to");
            const startDate = Date.parse(dateRange[0]);
            const endDate = Date.parse(dateRange[1]);
            return Date.parse(data) >= startDate && Date.parse(data) <= endDate;
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
                Object.entries(this.getEmptyEvent()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(this.getEmptyEvent()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },

        async validateForm() {
            //Perform validation on the form.
            await this.$formulate.submit("event-formulate-form-1");

            const vue_formulate_valid = this.$refs["event-formulate-form-1"].isValid;
            console.log('vue_formulate_valid', vue_formulate_valid)
            //vee-validate
            // await this.$validator.validate().then((result) => {
            //     return result
            // });

            //We could take the result. But we want to be explicit here.
            // let vee_validate_valid = (!this.veeErrors.has('multiselect-receivers'))

            return vue_formulate_valid;
        },
        assignFieldAsIdField(list, newIdFieldName, oldIdFieldName) {
            // For examplenew = 'user_id_fk' , old = 'id'
            // id : 3 and user_id_fk : 99 -> id : 99, user_id_fk : 99.  
            for (let i = 0; i < list.length; ++i) {
                list[i][oldIdFieldName] = list[i][newIdFieldName]
            }

            return list
        },

        cloneEventSettings() {

            let event = this.event
            let pastEvent = this.asyncSeachEventVariables.event

            if (typeof pastEvent.id === 'undefined')
                return;

            const shouldBeCopiedFields = [
                'start_datetime',
                'end_datetime',
                'used_for_calculation',
                'arranged_inside',
                'skills'];

            shouldBeCopiedFields.forEach((e) => {
                event[e] = pastEvent[e]
            });

            let today_date = (new Date()).toISOString().slice(0, 10) //yyyy-mm-dd
            let start_datetime_time_string = event.start_datetime.split("T")[1]
            let end_datetime_time_string = event.end_datetime.split("T")[1]
            // console.log(today_date)
            // console.log(start_datetime_time_string)

            event.start_datetime = today_date + "T" + start_datetime_time_string
            event.end_datetime = today_date + "T" + end_datetime_time_string
            // console.log(event.start_datetime)
            this.assignDataToEventForm(event);
        },
        _event_custom_label({ id, title }) {
            if (id === "" || id === null || typeof id === 'undefined') {
                return "Select";
            } else if (title === null || typeof title === "undefined") {

                const table = this.asyncSeachEventVariables.events
                for (let i = 0; i < table.length; ++i) {
                    if (table[i].id === id) {
                        const temp = table[i];
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.title}`;
                    }
                }
            }

            return `${id} ${title}`;
        },
        async asyncSearchEvent(event_search_term) {
            if (event_search_term === '' || event_search_term === null)
                return;

            const vars = this.asyncSeachEventVariables
            vars.isLoading = true

            if (typeof window.LIT !== 'undefined') {
                clearTimeout(window.LIT);
            }

            window.LIT = setTimeout(async () => {


                const searchParams = new URLSearchParams([
                    ['event_search_term', event_search_term]
                ]);

                await axios.get(this.$API_URL + "event/async-search", { params: searchParams }).then((response) => {
                    vars.events = response.data;
                    // console.log(this.user)
                });

                vars.isLoading = false


            }, 500); //setTimeout


        },
        _data_processing_for_test() {
            //Assume that the fields related to api calls are ready to be processed.
            this.event = this.getEmptyEvent();
            this._generate_formRender();
            // this.prepareData();
            // Rename for view multiselect. And backend receive list of dict of the field name id.
            // this.studentTable = this.assignFieldAsIdField(this.studentTable, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
            this.staffTable = this.assignFieldAsIdField(this.staffTable, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
        },
    },

    created: async function () {


        if (typeof this.testMode !== 'undefined') {
            this._data_processing_for_test()
            return;
        }

        this.event = this.getEmptyEvent();
        await axios.get(this.$API_URL + "user").then((response) => {
            this.user = response.data;
            // console.log(this.user)
        });
        this._generate_formRender();

        this.refreshData(); // get events

        axios.get(this.$API_URL + "staff").then((response) => {
            this.staffTable = this.assignFieldAsIdField(response.data, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
        });

        axios.get(this.$API_URL + "skillTable").then((response) => {
            this.skillTable = response.data;
            // console.log(this.skillTable)
        });

        this.$nextTick(() => {
            const inputs = [
                'input[placeholder="Filter Start"]',
                // 'input[placeholder="Filter Start Date"]'
                // 'input[placeholder="Filter Need By Date"]'
            ];

            inputs.forEach(function (input) {
                flatpickr(input, {
                    dateFormat: "d-m-Y",
                    mode: "range",
                    allowInput: true,
                    enableTime: true,
                });
            });

            document
                .getElementById("edit-info-modal")
                .addEventListener("hidden.bs.modal", (event) => {
                    this.veeErrors.clear();
                    this.formKey += 1;
                    this.asyncSeachEventVariables.events = []
                    this.asyncSeachEventVariables.event = null
                });
        })
    },

    mounted: function () {

    },
};
</script>

<template>
    <div>
        <h1 class="text-center">ระบบจัดเก็บการเข้าร่วมกิจกรรม</h1>

        <p>
            <button class="btn btn-primary" type="button" data-bs-toggle="collapse"
                data-bs-target="#query-parameters-collapse" aria-expanded="false" aria-controls="query-parameters-collapse">
                Query Parameters
            </button>
        </p>
        <div class="collapse" id="query-parameters-collapse">
            <div class="card card-body">
                <FormulateForm>
                    <h2 class="form-title">Query Parameters</h2>
                    <formulate-input type="vue-datetime" datetype="datetime" label="Lower bound start datetime"
                        v-model="queryParameters.lower_bound_start_datetime"></formulate-input>
                    <formulate-input type="vue-datetime" datetype="datetime" label="Upper bound start datetime"
                        v-model="queryParameters.upper_bound_start_datetime"></formulate-input>
                    <button @click="refreshData();" class="btn btn-primary">Query</button>
                </FormulateForm>
            </div>
        </div>

        <button v-if="!onlyAttendedByUser" type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal"
            data-bs-target="#edit-info-modal" @click="addClick()">
            Add Event
        </button>

        <vue-good-table ref="event-vgt" :columns="vgtColumns" :rows="events" :select-options="{
            enabled: false,
            selectOnCheckboxOnly: true, // only select when checkbox is clicked instead of the row
        }" :search-options="{ enabled: true }" :pagination-options="{
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
                    <!-- <input :checked="!column.hidden" type="checkbox" disabled/> -->

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="column.label + '-' + index"
                            href="#">
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
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="viewClick(props.row)">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button v-if="
                        user.is_staff ||
                        (!props.row.approved &&
                            props.row.created_by === user.id &&
                            user.is_student)
                    " type="button" :id="'edit-button-' + props.row.id" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="
                        user.is_staff ||
                        (!props.row.approved &&
                            props.row.created_by === user.id &&
                            user.is_student)
                    " type="button" @click="deleteClick(props.row.id)" class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>

        <div class="modal fade" id="edit-info-modal" tabindex="-1" data-bs-backdrop="static"
            aria-labelledby="edit-info-modal-label" aria-hidden="true">
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
                                <button v-if="!addingNewEvent" type="button" class="btn btn-primary m-2 fload-end"
                                    @click="showEventAttendanceModal = true" data-bs-toggle="modal"
                                    data-bs-target="#edit-info-modal">
                                    Show Attendances
                                </button>

                                <multiselect v-if="addingNewEvent && !modalReadonly"
                                    v-model="asyncSeachEventVariables.event" id="asyncSearchEventMultiselect"
                                    :custom-label="_event_custom_label" track-by="id"
                                    placeholder="Search and Clone the event settings" open-direction="bottom"
                                    :options="asyncSeachEventVariables.events" :multiple="false" :searchable="true"
                                    :loading="asyncSeachEventVariables.isLoading" :internal-search="false"
                                    :clear-on-select="false" :close-on-select="true" :options-limit="7" :limit="7"
                                    :max-height="600" :show-no-results="false" :hide-selected="true"
                                    @search-change="asyncSearchEvent">
                                    <span slot="noResult">No elements found. Consider changing the search query.</span>
                                </multiselect>
                                <button v-if="addingNewEvent && !modalReadonly" type="button"
                                    class="btn btn-primary m-2 fload-end" @click="cloneEventSettings();">Clone settings
                                </button>

                                <FormulateForm name="event-formulate-form-1" ref="event-formulate-form-1">
                                    <formulate-input ref="event-formulate-form-1-title" type="text" v-model="event.title"
                                        label="Title" validation="required|max:100"
                                        :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                                    <FormulateInput ref="event-formulate-form-1-start_datetime" type="vue-datetime"
                                        datetype="datetime" v-model="event.start_datetime" label="Start"
                                        validation="required" :disabled="modalReadonly || !formRender.edit.start_datetime">
                                    </FormulateInput>
                                    <FormulateInput ref="event-formulate-form-1-end_datetime" type="vue-datetime"
                                        datetype="datetime" v-model="event.end_datetime" label="End"
                                        validation="required|later" :validation-rules="{
                                            later: () => {
                                                return (
                                                    Date.parse(event.start_datetime) <
                                                    Date.parse(event.end_datetime)
                                                );
                                            },
                                        }" :validation-messages="{
    later: 'End datetime must be later than start datetime.',
}" error-behavior="live"
                                        :disabled="modalReadonly || !formRender.edit.end_datetime">
                                    </FormulateInput>
                                    <formulate-input ref="event-formulate-form-1-info" label="Info"
                                        :key="'event-formulate-form-1-info-' + formKey" type="textarea" v-model="event.info"
                                        validation="max:200,length" :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>

                                    <h6>Skills</h6>
                                    <multiselect ref="event-formulate-form-1-skills" v-model="event.skills"
                                        :hide-selected="true" :close-on-select="false" :multiple="true"
                                        :options="skillTable" :custom-label="_skills_custom_label" track-by="id"
                                        placeholder="Select..." :disabled="modalReadonly || !formRender.edit.skills">
                                    </multiselect>
                                    <p></p>
                                    <h6>Staffs</h6>
                                    <multiselect ref="event-formulate-form-1-staffs" v-model="event.staffs"
                                        :hide-selected="true" :close-on-select="false" :multiple="true"
                                        :options="staffTable" :custom-label="_staffs_custom_label" track-by="id"
                                        placeholder="Select..." :disabled="modalReadonly || !formRender.edit.staffs">
                                    </multiselect>

                                    <p></p>
                                    <FormulateInput ref="event-formulate-form-1-arranged_inside" v-model="checkboxes"
                                        :options="{ arranged_inside: 'Arranged inside' }" type="checkbox"
                                        :disabled="modalReadonly || !formRender.edit.arranged_inside"></FormulateInput>
                                    <FormulateInput ref="event-formulate-form-1-approved" v-model="checkboxes"
                                        :options="{ approved: 'approved' }" type="checkbox"
                                        :disabled="modalReadonly || !formRender.edit.approved"></FormulateInput>
                                    <FormulateInput ref="event-formulate-form-1-used_for_calculation" v-model="checkboxes"
                                        :options="{ used_for_calculation: 'Use for calculation' }" type="checkbox"
                                        :disabled="
                                            modalReadonly || !formRender.edit.used_for_calculation
                                        "></FormulateInput>
                                    <FormulateInput ref="event-formulate-form-1-attachment_link" type="url"
                                        v-model="event.attachment_link" label="Attachment link" placeholder="URL"
                                        validation="optional|url|max:200,length" help="optional" :disabled="
                                            modalReadonly || !formRender.edit.attachment_link
                                        ">
                                    </FormulateInput>

                                    <FormulateInput type="file" ref="event-formulate-form-1-attachment_file"
                                        :key="'event-formulate-form-1-attachment_file-' + formKey"
                                        v-model="event.attachment_file" label="Attachment file" error-behavior="live"
                                        validation-event="input" validation="optional|maxFileSize:2000000"
                                        upload-behavior="delayed" :disabled="
                                            modalReadonly || !formRender.edit.attachment_file
                                        " :validation-rules="{
    maxFileSize: (context, ...args) => {
        if (getFileOrNull(context.value) !== null)
            return context.value.files[0].file.size < parseInt(args[0]);
        return true;
    },
}" :validation-messages="{
    maxFileSize: (context) => {
        return 'The file size must not exceed ' + parseInt(context.args[0]) / (1000000) + ' mb.';
    },
}">

                                    </FormulateInput>
                                    <button v-if="(copiedEvent.attachment_file !== null)" type="button"
                                        class="btn btn-primary" @click="openNewWindow(copiedEvent.attachment_file)">
                                        File URL
                                    </button>
                                    <button v-if="(copiedEvent.attachment_file !== null)" type="button"
                                        class="btn btn-outline-danger" @click="
                                            copiedEvent.attachment_file = null;
                                        event.attachment_file = ''; formKey += 1;
                                                                                                              " :disabled="modalReadonly">
                                        Remove File
                                    </button>
                                </FormulateForm>
                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                            <button id="createButton" type="button" @click="createClick()" v-if="addingNewEvent"
                                class="btn btn-primary">
                                Create
                            </button>
                            <button v-if="!addingNewEvent && !modalReadonly" id="updateButton" type="button"
                                @click="updateClick()" class="btn btn-primary">
                                Update
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <EventAttendanceModal v-model="showEventAttendanceModal" :click-to-close="false">
            <template v-slot:title>Event Attendance</template>

            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showEventAttendanceModal = false" data-bs-toggle="modal" data-bs-target="#edit-info-modal">
                    Close
                </button></template>
            <EventAttendance v-if="!addingNewEvent && (typeof this.testMode === 'undefined')" :event_id="event.id"
                :user="user"></EventAttendance>
            <!-- <template v-slot:params><EventAttendance :event_id="event.id"></EventAttendance></template> -->
        </EventAttendanceModal>

        <div v-if="false" class="modal fade" id="event-attendance-modal" tabindex="-1" data-bs-backdrop="static"
            aria-labelledby="event-attendance-modal-label" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="event-attendance-modal-label">
                            Event Attendance
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">
                                <!-- <ATTENDANCE> -->
                                <EventAttendance :event_id="event.id"></EventAttendance>
                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
::v-deep .modal-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

::v-deep .modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    margin: 0 1rem;
    padding: 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    background: #fff;
}

.modal__title {
    margin: 0 2rem 0 0;
    font-size: 1.5rem;
    font-weight: 700;
}

.modal__close {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
}</style>
