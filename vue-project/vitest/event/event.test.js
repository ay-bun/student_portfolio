/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import Event from "./src/components/event/Event.vue";

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

const events = [{"id": 11, "title": "\u0e01\u0e34\u0e08\u0e01\u0e23\u0e23\u0e21\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e17\u0e31\u0e01\u0e29\u0e30\u0e01\u0e32\u0e23\u0e2a\u0e37\u0e48\u0e2d\u0e2a\u0e32\u0e23", "start_datetime": "2023-03-17T08:57", "end_datetime": "2023-03-21T18:57", "info": "", "created_by": 1, "approved": true, "approved_by": 1, "used_for_calculation": true, "arranged_inside": true, "attachment_link": "", "attachment_file": null, "skills": [{"id": 3}, {"id": 1}], "staffs": [{"id": 3}, {"id": 1}]}, {"id": 12, "title": "\u0e01\u0e34\u0e08\u0e01\u0e23\u0e23\u0e21\u0e1e\u0e31\u0e12\u0e19\u0e32\u0e17\u0e31\u0e01\u0e29\u0e30\u0e01\u0e32\u0e23\u0e2d\u0e2d\u0e01\u0e41\u0e1a\u0e1a", "start_datetime": "2023-02-01T09:08", "end_datetime": "2023-04-30T09:08", "info": "", "created_by": 1, "approved": true, "approved_by": 1, "used_for_calculation": true, "arranged_inside": false, "attachment_link": "", "attachment_file": null, "skills": [{"id": 4}, {"id": 6}, {"id": 5}], "staffs": [{"id": 3}]}, {"id": 16, "title": "\u0e2a\u0e31\u0e21\u0e19\u0e32\u0e04\u0e27\u0e32\u0e21\u0e01\u0e49\u0e32\u0e27\u0e2b\u0e19\u0e49\u0e32\u0e17\u0e32\u0e07\u0e40\u0e17\u0e04\u0e42\u0e19\u0e42\u0e25\u0e22\u0e35\u0e2d\u0e27\u0e01\u0e32\u0e28", "start_datetime": "2023-03-17T05:23", "end_datetime": "2023-03-25T05:24", "info": "", "created_by": 4, "approved": true, "approved_by": 1, "used_for_calculation": false, "arranged_inside": false, "attachment_link": "", "attachment_file": null, "skills": [{"id": 1}], "staffs": [{"id": 3}, {"id": 1}]}]
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

let event_formname = "event-formulate-form-1"
let ref_title = event_formname + "-" + "title"
let ref_start_datetime = event_formname + "-" + "start_datetime"
let ref_end_datetime = event_formname + "-" + "end_datetime"
let ref_info = event_formname + "-" + "info"
let ref_skills = event_formname + "-" + "skills"

let ref_staffs = event_formname + "-" + "staffs"
let ref_arranged_inside = event_formname + "-" + "arranged_inside" 
let ref_approved = event_formname + "-" + "approved"
let ref_used_for_calculation = event_formname + "-" + "used_for_calculation"
let ref_attachment_link = event_formname + "-" + "attachment_link"
let ref_attachment_file = event_formname + "-" + "attachment_file"

describe("Test event.", () => {
    //Concurrentcy
    //Set beforEach()???
    //Makesure that they donot mutate the data.??

    it("event-input-field-validation", async () => {
        const localVue = createLocalVue();
        localVue.use(VueFormulate, {
            plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
            mimes:{
              csv: 'text',
            },
        });

        localVue.use(VeeValidate, { errorBagName: "veeErrors" });
        const wrapper = mount(Event, {
            localVue,
            data() {
                return {

                    testMode: true, 

                    user: JSON.parse(JSON.stringify(user_staff)),
                    event: JSON.parse(JSON.stringify(events)),
                    // studentTable: JSON.parse(JSON.stringify(studentTable)),
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
        await wrapper.setData({ event: { title: "" } });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain("Title is required.");

        //title : max:100  || the string contains 101 characters.
        await wrapper.setData({  event: { title: "a".repeat(101), }, });
        
        title.performValidation();
        await flushPromises();
        console.log(wrapper.vm.event.title)
        expect(title.validationErrors).toContain(
            "Title must be less than or equal to 100 characters long."
        );
        //End Test : title

        
        //Test : start_date
        const start_datetime = wrapper.vm.$refs[ref_start_datetime];

        //start_datetime : required
        await wrapper.setData({ event: { start_datetime: "" } });
        start_datetime.performValidation();
        await flushPromises();
        expect(start_datetime.validationErrors).toContain(
            "Start is required."
        );
        //End start_date
        
        //Test end_date
        let end_date = wrapper.vm.$refs[ref_end_datetime];

        //end_date : required
        await wrapper.setData({ event: { end_datetime: "" } });
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain(
            "End is required."
        );
        
        //Endate 
        await wrapper.setData({ event: {  start_datetime: "2023-03-21T18:57", end_datetime: "2022-03-21T18:57" } });
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain(
            'End datetime must be later than start datetime.'
        );    

        
        //Test : info
        const info = wrapper.vm.$refs[ref_info];

        //info : string length || 204 chars
        await wrapper.setData({
            event: {
                info: "a".repeat(204),
            },
        });
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors).toContain(
            "Info must be less than or equal to 200 characters long."
        );
        // End info    
        
        //Test : attachment_link : url
        let attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ event: { attachment_link: "notalink" } });
        attachment_link.performValidation();
        await flushPromises();
        // console.log(attachment_link.validationErrors)
        expect(attachment_link.validationErrors).toContain('Please include a valid url.');
        
        attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ event: { attachment_link: "" } });
        attachment_link.performValidation();
        await flushPromises();
        // console.log(attachment_link.validationErrors.length)
        expect(attachment_link.validationErrors.length).toBe(0);
        
        attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ event: { attachment_link: '#'.repeat(201) } });
        attachment_link.performValidation();
        await flushPromises();
        expect(attachment_link.validationErrors).toContain('Attachment link must be less than or equal to 200 characters long.');
        //End attachment_link    

        //Test : attachment_file
        const attachment_file = wrapper.vm.$refs[ref_attachment_file];

        //attachment_file : maxFileSize
        await wrapper.setData({
            event: { attachment_file: { files: [{ file: { size: 2500000 } }] } },
        });
        attachment_file.performValidation();
        await flushPromises();
        // console.log(attachment_file.validationErrors)
        expect(attachment_file.validationErrors).toContain(
            "The file size must not exceed 2 mb."
        );
        //End attachment_file
    });

    it("event-form-submission",
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

            const wrapper = mount(Event, {
                localVue,
                data() {
                    return {
                        
                        testMode: true, 
                        
                        user: JSON.parse(JSON.stringify(user_staff)),
                        events: JSON.parse(JSON.stringify(events)),
                        // studentTable: JSON.parse(JSON.stringify(studentTable)),
                        staffTable: JSON.parse(JSON.stringify(staffTable)),
                        skillTable: JSON.parse(JSON.stringify(skillTable)),
                    };
                },
                // created : function(){}
            });
            await flushPromises()

            const valid_event_data = JSON.parse(JSON.stringify(events[0]))

            let invalids = {
                'title': "a".repeat(102),
                'start_datetime': '',
                'end_datetime': '',
                'info': "a".repeat(201),
                'attachment_link': 'notalink',
                'attachment_file' : { files: [{ file: { size: 2500000 } }]  },
            }
            
            // Test : valid data.
            wrapper.setData({
                event: JSON.parse(JSON.stringify(valid_event_data)),
            });

            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(true);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(true);
            });
            
            //Test title
            let copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['title'] = invalids['title'];
            await wrapper.setData({ event: copied_event });
            console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            
            //Test start_datetime
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['start_datetime'] = invalids['start_datetime'];
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            
            //Test start_datetime
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['end_datetime'] = invalids['end_datetime'];
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test info
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['info'] = invalids['info'];
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test attachment_link
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['attachment_link'] = invalids['attachment_link'];
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test attachment_link
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['attachment_file'] = invalids['attachment_file'];
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test : Start and End
            //     copied_event.start_datetime = "2023-03-21T18:57"
        //     copied_event.end_datetime = "2022-03-21T18:57"
            copied_event = JSON.parse(JSON.stringify(valid_event_data));
            copied_event['start_datetime'] = "2023-03-21T18:57"
            copied_event['end_datetime'] = "2022-03-21T18:57"
            await wrapper.setData({ event: copied_event });
            // console.log(copied_event)
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            


            // for (const [key, value] of Object.entries(invalids)) {
                
            //     const copied_event = JSON.parse(JSON.stringify(valid_event_data));
            //     copied_event[key.toString()] = value;
            //     // console.log([key, value])
            //     await wrapper.setData({ event: copied_event });
     
            //     await flushPromises();

            //     let formIsValid = true;
            //     await wrapper.vm.validateForm().then((result) => {
            //         formIsValid = result;
            //     });
            //     expect(formIsValid).toBe(false);
            // }

        //     // More than 1 field.
        //     const copied_event = JSON.parse(JSON.stringify(valid_event_data));
        //     copied_event.start_datetime = "2023-03-21T18:57"
        //     copied_event.end_datetime = "2022-03-21T18:57"
        //     await wrapper.setData({ event: copied_event });
        //     await flushPromises();
        //     let formIsValid = true;
        //         await wrapper.vm.validateForm().then((result) => {
        //             formIsValid = result;
        //         });
        //     expect(formIsValid).toBe(false);

        });
});
