<template>
    <div>
        <h1 class="text-center">ระบบการจัดการทักษะ</h1>
        
        <button v-if="false" type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
            Add Skill
        </button>

        <vue-good-table ref="skill-vgt" :columns="vgtColumns" :rows="skills"
            :select-options="{ enabled: false, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 10,
                setCurrentPage: 1,
            }" >

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

                    <button v-if="false" type="button" :id="'edit-button-' + props.row.id"
                        class="btn btn-light mr-1" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
                        @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <!-- <button v-if="user.is_staff"
                     type="button" @click="deleteClick(props.row.id)" class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button> -->
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>
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
                                <FormulateForm name="skill-formulate-form-1" ref="skill-formulate-form-1">
                                    <formulate-input ref="skill-formulate-form-1-title" type="text" v-model="skill.title"
                                        label="Title" validation="required|max:100"
                                        :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                                 <formulate-input ref="skill-formulate-form-1-info" label="Info"
                                        :key="'skill-formulate-form-1-info-' + formKey" type="textarea" v-model="skill.info"
                                        validation="max:200,length" :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>
                                </FormulateForm>
                            </div>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button id="createButton" type="button" @click="createClick()" v-if="addingNewSkill"
                            class="btn btn-primary">
                            Create
                        </button>
                        <!--                type="button" class="btn btn-primary"-->
                        <button type="button" class="btn btn-primary" v-if="
                            !modalReadonly &&
                            !addingNewSkill &&
                            (user.is_staff)

                        " id="updateButton" @click="updateClick()">
                            Update
                        </button>
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

// import flatpickr from "flatpickr";
// import "flatpickr/dist/flatpickr.min.css";
import * as bootstrap from "bootstrap";

export default {
    components: {
        VueGoodTable,
        // Multiselect,
    },

    data() {
        return {
            modalTitle: "",
            addingNewSkill: false,
            formKey: 1,

            user: {},
            skill: {},
            copiedSkill: {},
            skills: [],

            modalReadonly: false,

            formRender: {},

            variables: {
                API_URL: "",
            },

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
                    label: "Skill ID",
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
                    label: "Action",
                    field: "action",
                    thClass: "text-center",
                    tdClass: "text-center",
                },
            ],
        }

    },
    
    methods: {
        getEmptySkill() {
            return {
                id: 0,
                title: '',
                info:'',
            }
        },
        addClick() {
            this.modalTitle = "Add Skill";
            this.addingNewSkill = true; 
            this.modalReadonly = false;

            this.assignDataToSkillForm(this.getEmptySkill());
        },
        viewClick(skill) {
            this.modalTitle = "Read Only Mode";
            this.addingNewSkill = false;
            this.modalReadonly = true;

            this.assignDataToSkillForm(skill);
        },
        editClick(skill) {
            this.modalTitle = "Edit Mode";
            this.addingNewSkill = false;
            this.modalReadonly = false;

            this.assignDataToSkillForm(skill);
        },
        assignDataToSkillForm(skill) {
            const stringified = JSON.stringify(skill);
            this.skill = JSON.parse(stringified);
            this.copiedSkill = JSON.parse(stringified);
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

            const outForm = new FormData();
            const formData = this.skill
            for (const [key, value] of Object.entries(formData)) {
                outForm.append(key.toString(), value);
            }
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "skillTable",
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
                this.skills.push(data);
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

            const outForm = new FormData();
            const formData = this.skill
            for (const [key, value] of Object.entries(formData)) {
                outForm.append(key.toString(), value);
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.$API_URL + "skillTable/" + this.skill.id,
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
                this.reassignUpdatedElementIntoList(this.skills, data); //With reactivity.
                this.editClick(data)
                // alert(detail + '\n' + JSON.stringify(data));
                alert(detail);
            }).catch((error) => {
                alert(error.response.data.detail);
            });
        },
        async validateForm() {
            //Perform validation on the form.
            await this.$formulate.submit("skill-formulate-form-1");

            const vue_formulate_valid = this.$refs["skill-formulate-form-1"].isValid;
            console.log('vue_formulate_valid', vue_formulate_valid)
            return vue_formulate_valid;
        },
        reassignUpdatedElementIntoList(list, element) {
            for (let i = 0; i < list.length; ++i) {
                if (list[i].id === element.id) {
                    this.$set(list, i, element);
                    break;
                }
            }
        },
        _generate_formRender() {
            //Generate edit
            const user = this.user;
            let edit_info = {};
            const getEmptyElementFunction = this.getEmptySkill

            if (user.is_staff) {
                edit_info = this.formRenderSpec["staff"]["edit"];
            } else if (user.is_student) {
                edit_info = this.formRenderSpec["student"]["edit"];
            }

            const formRender = {};
            formRender["edit"] = {};

            if (edit_info["mode"] === "exclude") {
                Object.entries(getEmptyElementFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(getEmptyElementFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },
    },

    created: async function () {
        if (typeof this.testMode !== "undefined") {
            this._generate_formRender()
            // this._data_processing_for_test();
            return;
        }

        this.variables.API_URL = this.$API_URL
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFToken";
        axios.defaults.withCredentials = true;

        this.skill = this.getEmptySkill()
        await axios.get(this.variables.API_URL + "user").then((response) => {
            this.user = response.data;
        })
        this._generate_formRender()
        //SKILL api

        axios.get(this.variables.API_URL + "skillTable").then((response) => {
            this.skills = response.data;
        });

        this.$nextTick(() => {

            document
                .getElementById("edit-info-modal")
                .addEventListener("hidden.bs.modal", (event) => {
                    // this.veeErrors.clear();
                    this.formKey += 1;
                });

            })
    }
    
}
</script>