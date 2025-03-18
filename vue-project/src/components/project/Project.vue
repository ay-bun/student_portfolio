<template>
  <div>
    <h1 class="text-center">ระบบเสนอโครงการ</h1>

    <p>
      <button class="btn btn-primary" type="button" data-bs-toggle="collapse"
              data-bs-target="#query-parameters-collapse"
              aria-expanded="false" aria-controls="query-parameters-collapse">
        Query Parameters
      </button>
    </p>
    <div class="collapse" id="query-parameters-collapse">
      <div class="card card-body">
        <FormulateForm>
          <h2 class="form-title">Query Parameters</h2>
          <formulate-input type="date" label="Lower bound start date"
                           v-model="queryParameters.lower_bound_start_date"></formulate-input>
          <formulate-input type="date" label="Upper bound start date"
                           v-model="queryParameters.upper_bound_start_date"></formulate-input>
          <button @click="refreshData();" class="btn btn-primary">Query</button>
        </FormulateForm>
      </div>
    </div>

    <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
      Propose Project
    </button>

    <!-- Table -->
    <vue-good-table ref="project-vgt" :columns="vgtColumns" :rows="projects"
                    :select-options="{ enabled: false, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
                    :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 10,
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
                <span v-if="props.column.field === 'action'">
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
                <FormulateForm name="project-formulate-form-1" ref="project-formulate-form-1"
                               #default="{ hasErrors }">
                  <formulate-input ref="project-formulate-form-1-title" type="text"
                                   v-model="project.title" label="Title" validation="required|max:100"
                                   :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                  <formulate-input ref="project-formulate-form-1-start_date" type="date"
                                   v-model="project.start_date" label="Start Date" validation="required"
                                   :readonly="modalReadonly || !formRender.edit.start_date"></formulate-input>
                  <formulate-input ref="project-formulate-form-1-end_date" type="date"
                                   v-model="project.end_date" label="End Date" validation="required|later"
                                   :validation-rules="{
                                            later: () => {
                                                return (
                                                    Date.parse(project.start_date) <
                                                    Date.parse(project.end_date)
                                                );
                                            },
                                        }" :validation-messages="{
    later: 'End date must be later than start date.'
}"
                                   :readonly="modalReadonly || !formRender.edit.end_date"></formulate-input>
                  <formulate-input ref="project-formulate-form-1-info" label="Info"
                                   :key="'project-formulate-form-1-input-info-' + formKey" type="textarea"
                                   v-model="project.info" validation="max:200,length"
                                   :readonly="modalReadonly || !formRender.edit.info"
                                   validation-name="info"></formulate-input>
                  <div class="skill">
                    <h6>Skills</h6>
                    <multiselect ref="project-formulate-form-1-skills" v-model="project.skills"
                                 :hide-selected="true" :close-on-select="false" :multiple="true"
                                 :options="skillTable" :custom-label="_skills_custom_label" track-by="id"
                                 placeholder="Select..." :disabled="modalReadonly || !formRender.edit.skills">
                    </multiselect>
                  </div>
                  <div class="staff">
                    <h6>Staffs</h6>
                    <multiselect ref="project-formulate-form-1-staffs" v-model="project.staffs"
                                 :hide-selected="true" :close-on-select="false" :multiple="true"
                                 :options="staffTable" :custom-label="_staffs_custom_label" track-by="id"
                                 placeholder="Select..." :disabled="modalReadonly || !formRender.edit.staffs">
                    </multiselect>
                  </div>
                  <p></p>
                  <div class="mb-3">
                    <FormulateInput ref="project-formulate-form-1-approved" v-model="checkboxes"
                                    :options="{ approved: 'approved' }" type="checkbox"
                                    :disabled="project.approved || modalReadonly || !formRender.edit.approved"></FormulateInput>
                    <FormulateInput ref="project-formulate-form-1-used_for_calculation"
                                    v-model="checkboxes" :options="{ used_for_calculation: 'Use for calculation' }"
                                    type="checkbox" :disabled="
                                                modalReadonly || !formRender.edit.used_for_calculation
                                            ">
                    </FormulateInput>
                  </div>
                  <FormulateInput ref="project-formulate-form-1-attachment_link" type="url"
                                  validation="optional|url|max:200,length" v-model="project.attachment_link"
                                  label="Attachment link" help="optional" :disabled="
                                            modalReadonly || !formRender.edit.attachment_link
                                        "></FormulateInput>
                  <FormulateInput type="file" :key="'project-formulate-form-1-attachment_file-' + formKey"
                                  ref="project-formulate-form-1-attachment_file" v-model="project.attachment_file"
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
                  <button v-if="(copiedProject.attachment_file !== null)" type="button"
                          class="btn btn-primary" @click="openNewWindow(copiedProject.attachment_file)">
                    File URL
                  </button>
                  <button v-if="(copiedProject.attachment_file !== null)" type="button"
                          class="btn btn-outline-danger"
                          @click="copiedProject.attachment_file = null; project.attachment_file = ''; formKey += 1;"
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
            <button id="createButton" type="button" @click="createClick()" v-if="addingNewProject"
                    class="btn btn-primary">
              Create
            </button>

            <button id="updateButton" type="button" @click="updateClick()" v-if="!addingNewProject && !modalReadonly"
                    class="btn btn-primary">
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

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import * as bootstrap from "bootstrap";

export default {
  components: {
    VueGoodTable,
    Multiselect
  },

  data() {
    return {
      modalTitle: "",
      addingNewProject: false,

      modalReadonly: false,
      formKey: 1,

      project: {},
      copiedProject: {},
      projects: [],

      staffTable: [],
      user: {},

      queryParameters: {
        lower_bound_start_date: "2024-01-01",
        upper_bound_start_date: "2028-12-30"
      },

      checkboxes: [],
      checkboxFields: ["approved", "used_for_calculation"],
      formRenderSpec: {
        staff: {
          edit: {
            mode: "exclude",
            fields: []
          }
        },

        student: {
          edit: {
            mode: "exclude",
            fields: ["used_for_calculation", "approved"]
          }
        }
      },

      formRender: {},

      vgtColumns: [
        {
          label: "Project ID",
          field: "id",
          // tooltip: '',
          thClass: "text-center",
          tdClass: "text-center",

          filterOptions: {
            styleClass: "class1", // class to be added to the parent th element
            enabled: true, // enable filter for this column
            placeholder: "Filter This Thing", // placeholder for filter input
            filterValue: "", // initial populated value for this filter
            filterDropdownItems: [] // dropdown (with selected values) instead of text input
            // filterFn: this.columnFilterFn, //custom filter function that
            // trigger: 'enter', //only trigger on enter not on keyup
          }
        },
        {
          label: "Title",
          field: "title",
          thClass: "text-center",

          filterOptions: {
            styleClass: "class1", // class to be added to the parent th element
            enabled: true, // enable filter for this column
            placeholder: "Filter This Thing", // placeholder for filter input
            filterValue: "", // initial populated value for this filter
            filterDropdownItems: [] // dropdown (with selected values) instead of text input
            // filterFn: this.columnFilterFn, //custom filter function that
            // trigger: 'enter', //only trigger on enter not on keyup
          }
        },
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
            filterFn: this.dateRangeFilter
          }
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
            filterFn: this.dateRangeFilter
          }
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
            trigger: "enter" //only trigger on enter not on keyup
          }
        },
        {
          label: "Action",
          field: "action",
          thClass: "text-center",
          tdClass: "text-center"
        }
      ]
    };
  },

  methods: {
    getEmptyProject() {
      return {
        id: 0,
        title: "",
        start_date: "",
        end_date: "",

        info: "",

        created_by: "",
        approved: false,
        approved_by: "",
        used_for_calculation: false,

        attachment_link: "",
        attachment_file: null,

        skills: [],
        staffs: []
      };
    },

    refreshData() {
      const searchParams = new URLSearchParams([["lower_bound_start_date", this.queryParameters.lower_bound_start_date],
        ["upper_bound_start_date", this.queryParameters.upper_bound_start_date]]);
      axios.get(this.$API_URL + "project", { params: searchParams }).then((response) => {
        this.projects = response.data;
      });
    },

    addClick() {
      this.modalTitle = "Add Project";
      this.addingNewProject = true; // Signal that we are adding new project.
      this.modalReadonly = false;

      this.assignDataToProjectForm(this.getEmptyProject());
      console.log(this.project);
    },
    viewClick(project) {
      this.modalTitle = "Project (read only mode)";
      this.addingNewProject = false;
      this.modalReadonly = true;

      this.assignDataToProjectForm(project);
    },
    editClick(project) {
      this.modalTitle = "Edit project";
      this.addingNewProject = false;
      this.modalReadonly = false;

      this.assignDataToProjectForm(project);
    },
    assignDataToProjectForm(project) {
      const stringified = JSON.stringify(project);
      this.project = JSON.parse(stringified);
      this.copiedProject = JSON.parse(stringified);
      this.checkboxes = this.getListOfTrueCheckboxFields(
        this.project,
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

      this.assignBooleanValueToCheckboxFields(
        this.project,
        this.checkboxes,
        this.checkboxFields
      );
      const outForm = new FormData();
      for (const [key, value] of Object.entries(this.project)) {
        outForm.append(key.toString(), value);
      }
      outForm.set(
        "attachment_file",
        this.cleanAttachmentFile(this.project.attachment_file)
      );
      outForm.set(
        "skills",
        JSON.stringify(this.cleanManyToManyFields(this.project.skills))
      );
      outForm.set(
        "staffs",
        JSON.stringify(this.cleanManyToManyFields(this.project.staffs))
      );

      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios({
        method: "post",
        url: this.$API_URL + "project",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: outForm,
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": "csrftoken"
        }
      })
        .then((response) => {
          const data = response.data.data;
          const detail = response.data.detail;
          this.projects.push(data);
          this.editClick(data);

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

      if (typeof this.testMode !== "undefined") {
        return formIsValid;
      }

      if (!formIsValid) return;

      this.assignBooleanValueToCheckboxFields(
        this.project,
        this.checkboxes,
        this.checkboxFields
      );

      const outForm = new FormData();
      for (const [key, value] of Object.entries(this.project)) {
        outForm.append(key.toString(), value);
      }
      outForm.set(
        "attachment_file",
        this.cleanAttachmentFile(this.project.attachment_file)
      );
      outForm.set(
        "skills",
        JSON.stringify(this.cleanManyToManyFields(this.project.skills))
      );
      outForm.set(
        "staffs",
        JSON.stringify(this.cleanManyToManyFields(this.project.staffs))
      );

      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios({
        method: "put",
        url: this.$API_URL + "project/" + this.project.id,
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        data: outForm,
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": "csrftoken"
        }
      }).then((response) => {
        const data = response.data.data;
        const detail = response.data.detail;
        this.reassignUpdatedElementIntoList(this.projects, data); //With reactivity.
        this.editClick(data);

        // alert(detail + '\n' + JSON.stringify(data) );
        alert(detail);
      }).catch((error) => {
        alert(error.response.data.detail);
      });
    },
    deleteClick(project_id) {
      if (!confirm("Are you sure?")) {
        return;
      }

      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios({
        method: "delete",
        url: this.$API_URL + "project/" + project_id,
        xstfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        headers: {
          "X-CSRFToken": "csrftoken"
        }
      }).then((response) => {
        this.removeElementFromArrayById(this.projects, project_id);
        alert(response.data.detail);
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

    onFileSelected(event) {
      this.project.attachment_file = event.target.files[0];
    },
    prepareData() {
      this.project = this.getEmptyProject();
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
    async validateForm() {
      //Perform validation on the form.
      await this.$formulate.submit("project-formulate-form-1");

      const vue_formulate_valid =
        this.$refs["project-formulate-form-1"].isValid;

      //vee-validate
      // await this.$validator.validate().then((result) => {
      //     return result
      // });

      //We could take the result. But we want to be explicit here.
      // let vee_validate_valid = (!this.veeErrors.has('multiselect-receivers'))

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
        Object.entries(this.getEmptyProject()).forEach(([key, _]) => {
          formRender.edit[key.toString()] = !edit_info.fields.includes(key);
        });
      } else if (edit_info["mode"] === "include") {
        Object.entries(this.getEmptyProject()).forEach(([key, _]) => {
          formRender.edit[key.toString()] = edit_info.fields.includes(key);
        });
      } else {
        throw "The mode must be in { exlude, include }.";
      }

      this.formRender = formRender;
    },
    _skills_custom_label({ id, title }) {
      if (id === "" || Object.is(id, null)) {
        return "Select";
      } else if (Object.is(title, null) || typeof title === "undefined") {
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
    openNewWindow(url) {
      window.open(url);
    },
    assignFieldAsIdField(list, newIdFieldName, oldIdFieldName) {
      // For example new = 'user_id_fk' , old = 'id'
      // id : 3 and user_id_fk : 99 -> id : 99, user_id_fk : 99.
      for (let i = 0; i < list.length; ++i) {
        list[i][oldIdFieldName] = list[i][newIdFieldName];
      }

      return list;
    },
    _data_processing_for_test() {
      //Assume that the fields related to api calls are ready to be processed.
      this._generate_formRender();
      this.prepareData();
      // Rename for view multiselect. And backend receive list of dict of the field name id.
      // this.studentTable = this.assignFieldAsIdField(this.studentTable, 'user_id_fk', 'id') // Now, row.id === row.user_id_fk
      this.staffTable = this.assignFieldAsIdField(this.staffTable, "user_id_fk", "id"); // Now, row.id === row.user_id_fk
    }
  },

  created: async function() {

    if (typeof this.testMode !== "undefined") {
      this._data_processing_for_test();
      return;
    }

    this.prepareData();
    await axios.get(this.$API_URL + "user").then((response) => {
      this.user = response.data;
    });

    this._generate_formRender();

    // axios.get(this.$API_URL + "project").then((response) => {
    //     this.projects = response.data;
    // });
    this.refreshData();

    axios.get(this.$API_URL + "staff").then((response) => {
      this.staffTable = this.assignFieldAsIdField(response.data, "user_id_fk", "id");
    });

    axios.get(this.$API_URL + "skillTable").then((response) => {
      this.skillTable = response.data;
    });

    this.$nextTick(() => {
      const inputs = [
        // 'input[placeholder="Filter Received"]',
        "input[placeholder=\"Filter Start Date\"]",
        "input[placeholder=\"Filter End Date\"]"
      ];

      inputs.forEach(function(input) {
        flatpickr(input, {
          dateFormat: "d-m-Y",
          mode: "range",
          allowInput: true
          // enableTime:true,
        });
      });

      document
        .getElementById("edit-info-modal")
        .addEventListener("hidden.bs.modal", (event) => {
          this.veeErrors.clear();
          this.formKey += 1;
        });
    });
  },
  mounted: function() {


  }
};
</script>
