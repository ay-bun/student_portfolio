/**
 * @vitest-environment jsdom
*/


import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import Skill from "./src/components/profile/Skill.vue";

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

const skillTable = [{"id": 1, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 1", "info": "\u0e17\u0e31\u0e01\u0e2a\u0e23\u0e30\u0e30\u0e30"}, {"id": 2, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 2", "info": ""}, {"id": 3, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 3", "info": ""}, {"id": 4, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 4", "info": ""}, {"id": 5, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 5 \u0e17\u0e31\u0e01\u0e29\u0e30\u0e01\u0e32\u0e23\u0e17\u0e31\u0e01\u0e17\u0e32\u0e22", "info": "\u0e40\u0e25\u0e22\u0e21\u0e35\u0e41\u0e04\u0e48\u0e04\u0e33\u0e16\u0e32\u0e21\u0e42\u0e07\u0e48\u0e42\u0e07\u0e48\u0e1b\u0e34\u0e14\u0e1a\u0e31\u0e07\u0e40\u0e23\u0e37\u0e48\u0e2d\u0e07\u0e17\u0e35\u0e48\u0e0b\u0e48\u0e2d\u0e19\u0e43\u0e19\u0e43\u0e08 \u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e25\u0e36\u0e01 \u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e0b\u0e36\u0e49\u0e07 \u0e44\u0e21\u0e48\u0e44\u0e14\u0e49\u0e2a\u0e21\u0e04\u0e27\u0e32\u0e21\u0e04\u0e34\u0e14\u0e16\u0e36\u0e07\u0e17\u0e35\u0e48\u0e40\u0e01\u0e47\u0e1a\u0e44\u0e27\u0e49"}, {"id": 6, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 6  \u0e17\u0e31\u0e01\u0e29\u0e30\u0e01\u0e32\u0e23\u0e15\u0e37\u0e48\u0e19\u0e40\u0e0a\u0e49\u0e32", "info": "\u0e01\u0e32\u0e23\u0e1e\u0e31\u0e01\u0e1c\u0e48\u0e2d\u0e19\u0e40\u0e1b\u0e47\u0e19\u0e40\u0e23\u0e37\u0e48\u0e2d\u0e07\u0e17\u0e35\u0e48\u0e2a\u0e33\u0e04\u0e31\u0e0d \u0e01\u0e16\u0e49\u0e32\u0e40\u0e23\u0e32\u0e1e\u0e31\u0e01\u0e1c\u0e48\u0e2d\u0e19\u0e40\u0e23\u0e32\u0e01\u0e47\u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e17\u0e33\u0e07\u0e32\u0e19\ud83d\udc39"}, {"id": 7, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 7 \u0e17\u0e31\u0e01\u0e29\u0e30\u0e01\u0e32\u0e23\u0e1b\u0e25\u0e48\u0e2d\u0e22\u0e27\u0e32\u0e07\ud83e\udd5a", "info": "\u0e01\u0e47\u0e41\u0e04\u0e48\u0e17\u0e34\u0e49\u0e07\u0e21\u0e31\u0e19\u0e44\u0e1b \u0e1e\u0e23\u0e38\u0e48\u0e07\u0e19\u0e35\u0e49\u0e40\u0e23\u0e34\u0e48\u0e21\u0e43\u0e2b\u0e21\u0e48\u0e2d\u0e35\u0e01\u0e04\u0e27\u0e31\u0e49\u0e07"}, {"id": 8, "title": "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e04\u0e27\u0e32\u0e21\u0e2b\u0e49\u0e32\u0e27\u0e2b\u0e32\u0e0d", "info": ""}]

const localVue = createLocalVue();
            localVue.use(VueFormulate, {
                plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
                mimes:{
                  csv: 'text',
                },
            });
            localVue.use(VeeValidate, { errorBagName: "veeErrors" });

const skill_formname = "skill-formulate-form-1";
const ref_title = skill_formname + '-' + 'title'
const ref_info = skill_formname + '-' + 'info'

describe("Test Skill", () => {
    it("skill-input-field-validation", async () => {
        const wrapper = mount(Skill, {
            localVue,
            data() {
                return {
                    skill: {}, 
                    testMode: true, //Block api calls,
    
                    user: JSON.parse(JSON.stringify(user_staff)),
    
                    skills: JSON.parse(JSON.stringify(skillTable)),
                };
            },
            // created : function(){}
        });

        //Test : title
        const title = wrapper.vm.$refs[ref_title];

        // title : required
        await wrapper.setData({ skill: { title: "" } });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain("Title is required.");

        //title : max:100  || the string contains 101 characters.
        await wrapper.setData({
            skill: {
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

        //Test : info
        const info = wrapper.vm.$refs[ref_info];

        //info : || 201 chars
        await wrapper.setData({
            skill: {
                info: "",
            },
        });
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors.length).toBe(0);

        await wrapper.setData({
            skill: {
                info: "a".repeat(201),
            },
        });
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors).toContain(
            "Info must be less than or equal to 200 characters long."
        );
        //End info
            
    });
    

    it("skill-form-submission", async () => {

        const wrapper = mount(Skill, {
            localVue,
            data() {
                return {
                    skill: {}, 
                    testMode: true, //Block api calls,
    
                    user: JSON.parse(JSON.stringify(user_staff)),
    
                    skills: JSON.parse(JSON.stringify(skillTable)),
                };
            },
            // created : function(){}
        });

        await flushPromises()

        let valid_data = JSON.parse(JSON.stringify(skillTable[0]))
        
        let invalids = {
            'title': "a".repeat(101),
            'info': "a".repeat(201),
        }
        
        // Test : valid data.
        wrapper.setData({ skill : JSON.parse(JSON.stringify(valid_data)) });
        // console.log(wrapper.vm.skill)
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(true);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(true);
        })

        // Test : title
        let copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['title'] = invalids['title'];
        wrapper.setData({ skill : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        // Test : info
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['info'] = invalids['info'];
        wrapper.setData({ skill : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })
        
    });



});