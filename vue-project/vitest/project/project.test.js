/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import Project from "./src/components/project/Project.vue";

import FormulateVueDatetimePlugin from "@cone2875/vue-formulate-datetime";
import FormulateVSelectPlugin from '@cone2875/vue-formulate-select';
import VueFormulate from "@braid/vue-formulate";

import * as VeeValidate from "vee-validate";

const user_staff = {
    is_staff: true,
    is_student: false,
    groups: ["staff"],
    id: 1,
    is_authenticated: true,
    university_id: "623021038-1",
};

const projects = [{"id": 11, "title": "\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23\u0e2a\u0e48\u0e07\u0e40\u0e2a\u0e23\u0e34\u0e21\u0e2a\u0e38\u0e02\u0e20\u0e32\u0e1e", "start_date": "2023-03-18", "end_date": "2023-03-19", "info": "", "created_by": 1, "approved": true, "approved_by": 1, "used_for_calculation": true, "attachment_link": "", "attachment_file": null, "skills": [], "staffs": [{"id": 1}]}, {"id": 22, "title": "\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23\u0e2a\u0e48\u0e07\u0e40\u0e2a\u0e23\u0e34\u0e21\u0e27\u0e34\u0e0a\u0e32\u0e01\u0e32\u0e23", "start_date": "2023-03-17", "end_date": "2023-04-09", "info": "", "created_by": 1, "approved": true, "approved_by": 1, "used_for_calculation": true, "attachment_link": "", "attachment_file": null, "skills": [{"id": 1}], "staffs": [{"id": 1}]}, {"id": 23, "title": "\u0e42\u0e04\u0e23\u0e07\u0e01\u0e32\u0e23\u0e2a\u0e48\u0e07\u0e40\u0e2a\u0e23\u0e34\u0e21\u0e01\u0e32\u0e23\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e1a\u0e38\u0e04\u0e25\u0e34\u0e01\u0e20\u0e32\u0e1e", "start_date": "2023-03-10", "end_date": "2023-04-02", "info": "", "created_by": 1, "approved": true, "approved_by": 1, "used_for_calculation": false, "attachment_link": "", "attachment_file": null, "skills": [{"id": 2}, {"id": 1}], "staffs": [{"id": 3}, {"id": 1}]}]
const studentTable = [
    {
        id: 3,
        university_id: "623021039-1",
        user_id_fk: 2,
        firstname: "Tubtim",
        middlename: "",
        lastname: "Tubtim",
        faculty_role: 2,
        enroll: 1,
    },
    {
        id: 4,
        university_id: "623021039-2",
        user_id_fk: 4,
        firstname: "Tam",
        middlename: "",
        lastname: "Tam",
        faculty_role: 2,
        enroll: 1,
    },
];
const staffTable = [
    {
        id: 2,
        university_id: "623021038-2",
        user_id_fk: 3,
        firstname: "Toto",
        middlename: "",
        lastname: "Toto",
        faculty_role: 1,
    },
    {
        id: 1,
        university_id: "623021038-1",
        user_id_fk: 1,
        firstname: "Tuta",
        middlename: "",
        lastname: "Tuta",
        faculty_role: 1,
    },
];
const skillTable = [
    { id: 1, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 1" },
    { id: 2, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 2" },
    { id: 3, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 3" },
    { id: 4, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 4" },
    { id: 5, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 5" },
    { id: 6, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 6" },
];

let project_formname = "project-formulate-form-1"
let ref_title = project_formname + "-" + "title"
let ref_start_date = project_formname + "-" + "start_date"
let ref_end_date = project_formname + "-" + "end_date"
let ref_info = project_formname + "-" + "info"
let ref_skills = project_formname + "-" + "skills"

let ref_staffs = project_formname + "-" + "staffs"
let ref_approved = project_formname + "-" + "approved"
let ref_used_for_calculation = project_formname + "-" + "used_for_calculation"
let ref_attachment_link = project_formname + "-" + "attachment_link"
let ref_attachment_file = project_formname + "-" + "attachment_file"

describe("Test project.", () => {
    //Concurrentcy
    //Set beforEach()???
    //Makesure that they donot mutate the data.??

    it("project-input-field-validation", async () => {
        const localVue = createLocalVue();
        localVue.use(VueFormulate, {
            plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
            mimes:{
              csv: 'text',
            },
        });

        localVue.use(VeeValidate, { errorBagName: "veeErrors" });
        const wrapper = mount(Project, {
            localVue,
            data() {
                return {
                    project: {}, // This is the input
                    testMode: true, //Skill api calls in the award component.

                    user: JSON.parse(JSON.stringify(user_staff)),
                    projects: JSON.parse(JSON.stringify(projects)),
                    studentTable: JSON.parse(JSON.stringify(studentTable)),
                    staffTable: JSON.parse(JSON.stringify(staffTable)),
                    skillTable: JSON.parse(JSON.stringify(skillTable)),
                };
            },
            // created : function(){}
        });

        // const formulate_form = wrapper.vm.$refs[award_formname];

        //Test : title
        const title = wrapper.vm.$refs[ref_title];

        // title : required
        await wrapper.setData({ project: { title: "" } });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain("Title is required.");

        //title : max:100  || the string contains 102 characters.
        await wrapper.setData({
            project: {
                title:
                    "a".repeat(101),
            },
        });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain(
            "Title must be less than or equal to 100 characters long."
        );
        //End Test : title

        
        //Test : start_date
        const start_date = wrapper.vm.$refs[ref_start_date];

        //start_date : required
        await wrapper.setData({ project: { start_date: "" } });
        start_date.performValidation();
        await flushPromises();
        expect(start_date.validationErrors).toContain(
            "Start Date is required."
        );
        //End start_date
        
        //Test end_date
        let end_date = wrapper.vm.$refs[ref_end_date];

        //end_date : required
        await wrapper.setData({ project: { end_date: "" } });
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain(
            "End Date is required."
        );
        
        //Endate 
        await wrapper.setData({ project: {  start_date: "2023-03-18", end_date: "2023-03-17" } });
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain(
            "End date must be later than start date."
        );    


        //Test : info
        const info = wrapper.vm.$refs[ref_info];

        //info : string length || 204 chars
        await wrapper.setData({
            project: {
                info: "a".repeat(204),
            },
        });
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors).toContain(
            "Info must be less than or equal to 200 characters long."
        );


        //Test : attachment_link : url
        let attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ project: { attachment_link: "notalink" } });
        attachment_link.performValidation();
        await flushPromises();
        // console.log(attachment_link.validationErrors)
        expect(attachment_link.validationErrors).toContain('Please include a valid url.');
        
        attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ project: { attachment_link: "" } });
        attachment_link.performValidation();
        await flushPromises();
        // console.log(attachment_link.validationErrors.length)
        expect(attachment_link.validationErrors.length).toBe(0);

        attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ project: { attachment_link: '#'.repeat(201) } });
        attachment_link.performValidation();
        await flushPromises();
        expect(attachment_link.validationErrors).toContain('Attachment link must be less than or equal to 200 characters long.');
        //End attachment_link    

        //Test : attachment_file
        const attachment_file = wrapper.vm.$refs[ref_attachment_file];

        //attachment_file : maxFileSize
        await wrapper.setData({
            project: { attachment_file: { files: [{ file: { size: 2500000 } }] } },
        });
        attachment_file.performValidation();
        await flushPromises();
        // console.log(attachment_file.validationErrors)
        expect(attachment_file.validationErrors).toContain(
            "The file size must not exceed 2 mb."
        );
    });

    it("project-form-submission",
        async () => {
            //
            // Condition 1 : All fields, except one field, are valid. 
            // Condition 2 : More than 1 field (Done).
            // Expected behavior :  Form should not be submitted.
            const localVue = createLocalVue();
            localVue.use(VueFormulate, {
                plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
                mimes:{
                  csv: 'text',
                },
            });
            localVue.use(VeeValidate, { errorBagName: "veeErrors" });
            const wrapper = mount(Project, {
                localVue,
                data() {
                    return {
                        project: {}, // This is the input
                        testMode: true, 
                        

                        user: JSON.parse(JSON.stringify(user_staff)),
                        projects: JSON.parse(JSON.stringify(projects)),
                        studentTable: JSON.parse(JSON.stringify(studentTable)),
                        staffTable: JSON.parse(JSON.stringify(staffTable)),
                        skillTable: JSON.parse(JSON.stringify(skillTable)),
                    };
                },
                // created : function(){}
            });
            await flushPromises()

            const valid_data = JSON.parse(JSON.stringify(projects[0]))

            let invalids = {
                'title': "a".repeat(101),
                'start_date': '',
                'end_date': '',
                'info': "a".repeat(201),
                'attachment_link': 'notalink',
                'attachment_file' : { files: [{ file: { size: 2500000 } }]  },
            }
            
            // Test : valid data.
            wrapper.setData({
                project: JSON.parse(JSON.stringify(valid_data)),
            });

            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(true);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(true);
            });

            //Test title
            let copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['title'] = invalids['title'];
            await wrapper.setData({ project: copied_data });
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            
            //Test start_date
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['start_date'] = invalids['start_date'];
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test end_date
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['end_date'] = invalids['end_date'];
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            
            //Test info
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['info'] = invalids['info'];
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test attachment_link
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['attachment_link'] = invalids['attachment_link'];
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test attachment_file
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['attachment_file'] = invalids['attachment_file'];
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['start_date'] = "2023-03-18";
            copied_data['end_date'] = "2023-03-18";
            await wrapper.setData({ project: copied_data });
            // console.log(copied_data)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });


            // expect(temp_bool_val).toBe(true);
            
            // for (const [key, value] of Object.entries(invalids)) {
                
            //     const copied_project = JSON.parse(JSON.stringify(valid_project_data));
            //     copied_project[key.toString()] = value;
            //     // console.log([key, value])
            //     await wrapper.setData({ project: copied_project });
     
            //     await flushPromises();

            //     let formIsValid = true;
            //     await wrapper.vm.validateForm().then((result) => {
            //         formIsValid = result;
            //     });
            //     expect(formIsValid).toBe(false);
            // }

            // // More than 1 field.
            // const copied_project = JSON.parse(JSON.stringify(valid_project_data));
            // copied_project.start_date = "2023-03-18"
            // copied_project.end_date = "2023-03-18"
            // await wrapper.setData({ project: copied_project });
            // await flushPromises();
            // let formIsValid = true;
            // await wrapper.vm.validateForm().then((result) => {
            //     formIsValid = result;
            // });
            // expect(formIsValid).toBe(false);
            
        });
});
