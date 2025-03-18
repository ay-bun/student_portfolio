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
            modalTitle: "",
            addingNewAward: false,
            formKey: 1,
            showApproved: true,

            staffTable: [],
            studentTable: [], //Define user Api.

            user: {},

            award: {},
            copiedAward: {},
            awards: [],

            checkboxes: [],
            checkboxFields: ["approved", "used_for_calculation"],

            queryParameters: {
                lower_bound_received_date: "2024-01-01",
                upper_bound_received_date: "2028-12-01"
            },

            modalReadonly: false,

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
                    label: "Award ID",
                    field: "id",
                    // tooltip: "A simple tooltip",
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
                    label: "Title",
                    field: "title",
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
                    label: "Received date",
                    field: "received_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "yyyy-mm-dd",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Received",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "Approved",
                    field: "approved",
                    thClass: "text-center",
                    tdClass: "text-center",
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
        getEmptyAward() {
            return {
                id: 0,
                title: "",
                rank: 0,
                received_date: "",

                info: "",

                created_by: "",
                approved: false,
                approved_by: "",
                used_for_calculation: false,

                attachment_link: "",
                attachment_file: null,

                //many-to-many fields
                skills: [],
                receivers: [],
                supervisors: [],
            };
        },

        refreshData() {
            const searchParams = new URLSearchParams([['lower_bound_received_date', this.queryParameters.lower_bound_received_date],
            ['upper_bound_received_date', this.queryParameters.upper_bound_received_date]]);
            axios.get(this.$API_URL + "award", { params: searchParams }).then((response) => {
                this.awards = response.data;
            });
        },

        addClick() {
            this.modalTitle = "Add Award";
            this.addingNewAward = true; // Signal that we are adding new award.
            this.modalReadonly = false;

            this.assignDataToAwardForm(this.getEmptyAward());
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

            this.assignBooleanValueToCheckboxFields(
                this.award,
                this.checkboxes,
                this.checkboxFields
            );
            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.award)) {
                outForm.append(key.toString(), value);
            }
            outForm.set(
                "attachment_file",
                this.cleanAttachmentFile(this.award.attachment_file)
            );
            outForm.set(
                "skills",
                JSON.stringify(this.cleanManyToManyFields(this.award.skills))
            );
            outForm.set(
                "receivers",
                JSON.stringify(this.cleanManyToManyFields(this.award.receivers))
            );
            outForm.set(
                "supervisors",
                JSON.stringify(this.cleanManyToManyFields(this.award.supervisors))
            );

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "award",
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
                this.awards.push(data);
                this.editClick(data) //Change viewing mode.

                // alert(detail + '\n' + JSON.stringify(data));
                alert(detail);

            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },
        viewClick(award) {
            this.modalTitle = "Award (read only mode)";
            this.addingNewAward = false;
            this.modalReadonly = true;

            this.assignDataToAwardForm(award);
        },
        editClick(award) {
            this.modalTitle = "Edit award";
            this.addingNewAward = false;
            this.modalReadonly = false;

            this.assignDataToAwardForm(award);
        },

        assignDataToAwardForm(award) {
            const stringified = JSON.stringify(award);
            this.award = JSON.parse(stringified);
            this.copiedAward = JSON.parse(stringified);

            this.checkboxes = this.getListOfTrueCheckboxFields(
                this.award,
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
                this.award,
                this.checkboxes,
                this.checkboxFields
            );
            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.award)) {
                outForm.append(key.toString(), value);
            }
            outForm.set(
                "attachment_file",
                this.cleanAttachmentFile(this.award.attachment_file)
            );
            outForm.set(
                "skills",
                JSON.stringify(this.cleanManyToManyFields(this.award.skills))
            );
            outForm.set(
                "receivers",
                JSON.stringify(this.cleanManyToManyFields(this.award.receivers))
            );
            outForm.set(
                "supervisors",
                JSON.stringify(this.cleanManyToManyFields(this.award.supervisors))
            );

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.$API_URL + "award/" + this.award.id,
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
                this.reassignUpdatedElementIntoList(this.awards, data); //With reactivity.
                this.editClick(data)

                alert(detail + '\n' + JSON.stringify(data));
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },

        deleteClick(award_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url: this.$API_URL + "award/" + award_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.removeElementFromArrayById(this.awards, award_id);
                alert(response.data.detail)
            }).catch((error) => {
                alert(error.response.data.detail);
            });
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

        onFileSelected(event) {
            this.award.attachment_file = event.target.files[0];
        },

        prepareData() {
            this.award = this.getEmptyAward();
        },

        //custom labels
        skillCustomLabel({ id, title }) {
            if (id === "" || Object.is(id, null)) {
                return "Select";
            } else if (Object.is(title, null) || typeof title === "undefined") {
                for (let i = 0; i < this.skillTable.length; ++i) {
                    if (this.skillTable[i].id === id) {
                        const temp = this.skillTable[i];
                        return `${temp.id} ${temp.title}`;
                    }
                }
            }

            return `${id} ${title}`;
        },

        receiverCustomLabel({ id, university_id, firstname, lastname }) {
            if (id === "" || id === null || typeof id === 'undefined') {
                return "Select";
            } else if (university_id == null) {
                for (let i = 0; i < this.studentTable.length; ++i) {
                    if (this.studentTable[i].id === id) {
                        const temp = this.studentTable[i];
                        return `${temp.university_id} ${temp.firstname} ${temp.lastname}`;
                    }
                }
            }

            return `${university_id} ${firstname} ${lastname}`;
        },

        supervisorCustomLabel({ id, university_id, firstname, lastname }) {
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

        selectionChanged(params) {
            // console.log('heloo')
            // this.selectedRows = params.selectedRows
            // let selectedRows = this.$refs['vgt'].selectedRows
            // console.log(selectedRows)
            // console.log(params)
        },

        rowActionDelete() {
            const selectedRows = this.$refs["award-vgt"].selectedRows;
            // console.log(selectedRows);

            const ids = [];
            for (let i = 0; i < selectedRows.length; ++i) {
                ids.push(selectedRows[i].id);
            }

            const outForm = new FormData();
            outForm.append("ids", JSON.stringify(ids));

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url: this.$API_URL + "award/multi-delete",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();

                alert(response.data);
            });
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

        async validateForm() {
            //Perform validation on the form.
            await this.$formulate.submit("award-formulate-form-1");

            const vue_formulate_valid = this.$refs["award-formulate-form-1"].isValid;
            // console.log('vue_formulate_valid', vue_formulate_valid)
            //vee-validate scope : award
            let vee_validate_valid = false;
            await this.$validator.validateAll('award-formulate-form-1').then((result) => {
                vee_validate_valid = result;
            });
            // console.log('vee_validate_valid', vee_validate_valid)
            //We could take the result. But we want to be explicit here.
            // const vee_validate_valid = !this.veeErrors.has("multiselect-receivers");

            return vue_formulate_valid && vee_validate_valid;
        },

        openNewWindow(url) {
            window.open(url);
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
                Object.entries(this.getEmptyAward()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(this.getEmptyAward()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },

        renameKeyOfDictsInList(listOfDicts, newName, OldName) {
            for (let i = 0; i < listOfDicts.length; ++i) {
                let dict = listOfDicts[i]
                Object.defineProperty(dict, newName, Object.getOwnPropertyDescriptor(dict, OldName))
                delete dict[OldName];
            }
            return listOfDicts
        },
        assignFieldAsIdField(list, newIdFieldName, oldIdFieldName) {
            // For examplenew = 'user_id_fk' , old = 'id'
            // id : 3 and user_id_fk : 99 -> id : 99, user_id_fk : 99.  
            for (let i = 0; i < list.length; ++i) {
                list[i][oldIdFieldName] = list[i][newIdFieldName]
            }

            return list
        },


        _data_processing_for_test() {
            //Assume that the fields related to api calls are ready to be processed.
            this._generate_formRender();
            this.prepareData();
            // Rename for view multiselect. And backend receive list of dict of the field name id.
            this.studentTable = this.assignFieldAsIdField(this.studentTable, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
            this.staffTable = this.assignFieldAsIdField(this.staffTable, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
        },

    },

    created: async function () {

        if (typeof this.testMode !== "undefined") {
            this._data_processing_for_test();
            return;
        }

        this.prepareData(); // Assign an empty award.
        // console.log(documuent.cookies)
        // console.log("Hello from Award.Vue");
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFToken";
        axios.defaults.withCredentials = true;

        await axios.get(this.$API_URL + "user").then((response) => {
            this.user = response.data;
        })

        this._generate_formRender();

        this.refreshData();

        axios.get(this.$API_URL + "student").then((response) => {
            // this.studentTable = response.data;
            this.studentTable = this.assignFieldAsIdField(response.data, 'user_id_fk', 'id')
        });

        axios.get(this.$API_URL + "staff").then((response) => {
            // this.staffTable = response.data;
            this.staffTable = this.assignFieldAsIdField(response.data, 'user_id_fk', 'id')

        });

        axios.get(this.$API_URL + "skillTable").then((response) => {
            this.skillTable = response.data;
        });

        this.$nextTick(() => {

            const inputs = [
                'input[placeholder="Filter Received"]',
                // 'input[placeholder="Filter Start Date"]'
                // 'input[placeholder="Filter Need By Date"]'
            ];

            inputs.forEach(function (input) {
                flatpickr(input, {
                    dateFormat: "Y-m-d",
                    mode: "range",
                    allowInput: true,
                    // enableTime:true,
                });
            });

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

<template>
    <div>
        <h1 class="text-center">ระบบจัดเก็บรางวัล</h1>

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
                    <formulate-input type="date" label="Lower bound received date"
                        v-model="queryParameters.lower_bound_received_date"></formulate-input>
                    <formulate-input type="date" label="Upper bound received date"
                        v-model="queryParameters.upper_bound_received_date"></formulate-input>
                    <button @click="refreshData();" class="btn btn-primary">Query</button>
                </FormulateForm>
            </div>
        </div>

        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
            Add Award
        </button>


        <vue-good-table ref="award-vgt" :columns="vgtColumns" :rows="awards"
            :select-options="{ enabled: false, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 10,
                setCurrentPage: 1,
            }" @on-selected-rows-change="selectionChanged">
            <div slot="selected-row-actions">
                <button @click="rowActionDelete">delete</button>
            </div>

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

        <!--    <div class="modal fade" id="edit-info-modal" tabindex="-1"-->
        <div class="modal fade" id="edit-info-modal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false"
            aria-labelledby="ModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="ModalLabel">{{ modalTitle }}</h5>

                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-1 w-50 bd-highlight">
                                <FormulateForm name="award-formulate-form-1" ref="award-formulate-form-1"
                                    #default="{ hasErrors }">
                                    <formulate-input ref="award-formulate-form-1-title" type="text" v-model="award.title"
                                        label="Title" validation="required|max:100"
                                        :readonly="modalReadonly || !formRender.edit.title"></formulate-input>

                                    <formulate-input ref="award-formulate-form-1-rank" type="number" v-model="award.rank"
                                        label="Rank" validation="required|number|min:0"
                                        :readonly="modalReadonly || !formRender.edit.rank">
                                    </formulate-input>

                                    <formulate-input ref="award-formulate-form-1-received_date" type="date"
                                        v-model="award.received_date" label="Received Date" validation="required"
                                        :readonly="modalReadonly || !formRender.edit.received_date"></formulate-input>

                                    <formulate-input ref="award-formulate-form-1-info" label="Info"
                                        :key="'award-formulate-input-info-' + formKey" type="textarea" v-model="award.info"
                                        validation="max:200,length" :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>

                                    <div class="skill">
                                        <h6>Skills</h6>
                                        <multiselect ref="award-formulate-form-1-skills" v-model="award.skills"
                                            :hide-selected="true" :close-on-select="false" :multiple="true"
                                            :options="skillTable" :custom-label="skillCustomLabel" track-by="id"
                                            placeholder="Select..." :disabled="modalReadonly || !formRender.edit.skills">
                                        </multiselect>
                                    </div>

                                    <div class="receiver">
                                        <h6>Receivers</h6>
                                        <div>
                                            <multiselect ref="award-formulate-form-1-receivers" name="receivers"
                                                v-model="award.receivers" v-validate="'required|min:1'"
                                                data-vv-validate-on="input" data-vv-as="receivers"
                                                data-vv-scope="award-formulate-form-1" :hide-selected="true"
                                                :close-on-select="false" :multiple="true" :options="studentTable"
                                                :custom-label="receiverCustomLabel" track-by="user_id_fk"
                                                placeholder="Select..."
                                                :disabled="modalReadonly || !formRender.edit.receivers">
                                            </multiselect>
                                            <span v-show="veeErrors.has('award-formulate-form-1.receivers')"
                                                style="color: red">{{ veeErrors.first('award-formulate-form-1.receivers')
                                                }}</span>


                                        </div>
                                    </div>

                                    <div class="staff">
                                        <h6>Supervisors</h6>
                                        <multiselect ref="award-formulate-form-1-supervisors" v-model="award.supervisors"
                                            :hide-selected="true" :close-on-select="false" :multiple="true"
                                            :options="staffTable" :custom-label="supervisorCustomLabel" track-by="id"
                                            placeholder="Select..."
                                            :disabled="modalReadonly || !formRender.edit.supervisors"></multiselect>
                                    </div>

                                    <p></p>

                                    <div class="mb-3">
                                        <FormulateInput ref="award-formulate-form-1-approved" v-model="checkboxes"
                                            :options="{ approved: 'approved' }" type="checkbox"
                                            :disabled="modalReadonly || !formRender.edit.approved"></FormulateInput>
                                        <FormulateInput ref="award-formulate-form-1-used_for_calculation"
                                            v-model="checkboxes" :options="{ used_for_calculation: 'Use for calculation' }"
                                            type="checkbox" :disabled="
                                                modalReadonly || !formRender.edit.used_for_calculation
                                            "></FormulateInput>
                                    </div>

                                    <div class="mb-3">
                                        <FormulateInput ref="award-formulate-form-1-attachment_link" type="url"
                                            v-model="award.attachment_link" label="Attachment link" placeholder="URL"
                                            help="optional" validation="optional|url|max:200,length" :disabled="
                                                modalReadonly || !formRender.edit.attachment_link
                                            "></FormulateInput>
                                    </div>

                                    <p></p>

                                    <div class="mb-3">
                                        <FormulateInput type="file"
                                            :key="'award-formulate-form-1-attachment_file-' + formKey"
                                            ref="award-formulate-form-1-attachment_file" v-model="award.attachment_file"
                                            label="Attachment file" help="" :validation-rules="{
                                                maxFileSize: (context, ...args) => {
                                                    if (getFileOrNull(context.value) !== null)
                                                        return context.value.files[0].file.size < parseInt(args[0]);
                                                    return true;
                                                },
                                            }" :validation-messages="{
    maxFileSize: (context) => {
        return 'The file size must not exceed ' + parseInt(context.args[0]) / (1000000) + ' mb.';
    },
}" error-behavior="live" validation-event="input"
                                            validation="optional|maxFileSize:2000000" upload-behavior="delayed" :disabled="
                                                modalReadonly || !formRender.edit.attachment_file
                                            "></FormulateInput>
                                        <!--                            File Button-->
                                        <button v-if="(copiedAward.attachment_file !== null)" type="button"
                                            class="btn btn-primary" @click="openNewWindow(copiedAward.attachment_file)">
                                            File URL
                                        </button>
                                        <button v-if="(copiedAward.attachment_file !== null)" type="button"
                                            class="btn btn-outline-danger"
                                            @click="copiedAward.attachment_file = null; award.attachment_file = ''; formKey += 1;"
                                            :disabled="modalReadonly">
                                            Remove File
                                        </button>
                                    </div>

                                </FormulateForm>
                            </div>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button id="createButton" type="button" @click="createClick()" v-if="addingNewAward"
                            class="btn btn-primary">
                            Create
                        </button>
                        <!--                type="button" class="btn btn-primary"-->
                        <button type="button" class="btn btn-primary" v-if="
                            !modalReadonly &&
                            !addingNewAward &&
                            (user.is_staff ||
                                (user.is_student && award.created_by == user.id))
                        " id="updateButton" @click="updateClick()">
                            Update
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
