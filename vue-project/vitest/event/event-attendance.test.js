/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import EventAttendance from "./src/components/event/EventAttendance.vue";

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

const eventAttendances = [{"id": 228, "event_id_fk": 11, "university_id": "623021039-2", "firstname": "Tam", "middlename": "", "lastname": "Tam", "user_id_fk": 4, "synced": true, "used_for_calculation": true}, {"id": 229, "event_id_fk": 11, "university_id": "623021039-1", "firstname": "Tubtim", "middlename": "", "lastname": "Tubtim", "user_id_fk": 2, "synced": true, "used_for_calculation": true}]
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

let event_attendance_formname = "event-attendance-formulate-form-1"
let ref_university_id = event_attendance_formname + "-" + "university_id"
let ref_firstname = event_attendance_formname + "-" + "firstname"
let ref_middlename = event_attendance_formname + "-" + "middlename"
let ref_lastname = event_attendance_formname + "-" + "lastname"
let ref_used_for_calculation = event_attendance_formname + "-" + "used_for_calculation"

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
        const wrapper = mount(EventAttendance, {
            localVue,
            data() {
                return {

                    testMode: true, 
                
                    eventAttendances: JSON.parse(JSON.stringify(eventAttendances)),
                    studentTable: JSON.parse(JSON.stringify(studentTable)),

                };
            },
            // created : function(){}
            propsData: {
                user: JSON.parse(JSON.stringify(user_staff)),
            },
        });

        //Test : university_id
        // university_id : required
        await wrapper.setData({ eventAttendance: { university_id: null } });
        wrapper.vm.$validator.validateAll(event_attendance_formname);
        // title.performValidation();
        await flushPromises();
        expect(wrapper.vm.veeErrors.collect(event_attendance_formname + '.' + 'university_id')).toContain(
            "The university id field is required"
        );
        //End Test : title

        
        //Test : firstname
        const firstname = wrapper.vm.$refs[ref_firstname];

        //firstname : max:50
        await wrapper.setData({ eventAttendance: { firstname: "a".repeat(51) } });
        firstname.performValidation();
        await flushPromises();
        // console.log(firstname.validationErrors)
        expect(firstname.validationErrors).toContain(
            "Firstname must be less than or equal to 50 characters long."
        );
        //End firstname
        
        //Test middlename
        let middlename = wrapper.vm.$refs[ref_middlename];

        //end_date : required
        await wrapper.setData({ eventAttendance: { middlename: "a".repeat(51) } });
        middlename.performValidation();
        await flushPromises();
        // console.log(middlename.validationErrors)
        expect(middlename.validationErrors).toContain(
            "Middlename must be less than or equal to 50 characters long."
        );
        //End middlename  
        
        //Test lastname
        let lastname = wrapper.vm.$refs[ref_lastname];

        //end_date : required
        await wrapper.setData({ eventAttendance: { lastname: "a".repeat(51) } });
        lastname.performValidation();
        await flushPromises();
        // console.log(lastname.validationErrors)
        expect(lastname.validationErrors).toContain(
            "Lastname must be less than or equal to 50 characters long."
        );
        //End lastname
    });

    it("event-attendance-form-submission",
        async () => {
            //
            // Condition 1 : All fields, except one field, are valid. 
            // Expected behavior :  Form should not be submitted.
            const localVue = createLocalVue();
            localVue.use(VueFormulate, {
                plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
                mimes:{
                  csv: 'text',
                },
            });
            localVue.use(VeeValidate, { errorBagName: "veeErrors" });
            const wrapper = mount(EventAttendance, {
                localVue,
                data() {
                    return {
                        
                        testMode: true, 
                        
                        eventAttendances: JSON.parse(JSON.stringify(eventAttendances)),
                        studentTable: JSON.parse(JSON.stringify(studentTable)),

                    };
                },
                propsData: {
                    user: JSON.parse(JSON.stringify(user_staff)),
                },
            });

            await flushPromises()

            const valid_data = JSON.parse(JSON.stringify(eventAttendances[0]))
            valid_data.university_id = { university_id : valid_data.university_id}; //multiselect behave this way.

            let invalids = {
                'university_id' : null,
                'firstname': "a".repeat(51),
                'middlename': "a".repeat(51),
                'lastname': "a".repeat(51),
            }
            
            // Test : valid data.
            wrapper.setData({ eventAttendance: JSON.parse(JSON.stringify(valid_data)), });
            
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(true);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(true);
            });
            
            //Test university_id
            let copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['university_id'] = invalids['university_id'];
            wrapper.setData({ eventAttendance: copied_data, });
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test firstname
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['firstname'] = invalids['firstname'];
            wrapper.setData({ eventAttendance: copied_data, });
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test middlename
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['middlename'] = invalids['middlename'];
            wrapper.setData({ eventAttendance: copied_data, });
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });

            //Test middlename
            copied_data = JSON.parse(JSON.stringify(valid_data));
            copied_data['lastname'] = invalids['lastname'];
            wrapper.setData({ eventAttendance: copied_data, });
            await flushPromises();
            await wrapper.vm.createClick().then((result) => {
                expect(result).toBe(false);
            });
            await wrapper.vm.updateClick().then((result) => {
                expect(result).toBe(false);
            });
            
            //Test : invalid data
            // for (const [key, value] of Object.entries(invalids)) {
                
            //     const copied_data = JSON.parse(JSON.stringify(valid_data));
            //     copied_data[key.toString()] = value;
            //     // console.log([key, value])
            //     await wrapper.setData({ eventAttendance: copied_data });
                
            //     await flushPromises();

            //     let formIsValid = true;
            //     await wrapper.vm.validateForm().then((result) => {
            //         formIsValid = result;
            //         // console.log('in validate form')
            //     });
            //     expect(formIsValid).toBe(false);
            // }

        });
});
