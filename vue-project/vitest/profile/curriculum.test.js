/**
 * @vitest-environment jsdom
*/

import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import Curriculum from "./src/components/profile/Curriculum.vue";

import FormulateVueDatetimePlugin from "@cone2875/vue-formulate-datetime";
import FormulateVSelectPlugin from '@cone2875/vue-formulate-select';
import VueFormulate from "@braid/vue-formulate";

import * as VeeValidate from "vee-validate";


const localVue = createLocalVue();
localVue.use(VueFormulate, {
    plugins: [FormulateVueDatetimePlugin, FormulateVSelectPlugin ],
    mimes:{
        csv: 'text',
    },
});
localVue.use(VeeValidate, { errorBagName: "veeErrors" });

const user_staff = {
    is_staff: true,
    is_student: false,
    groups: ["staff"],
    id: 1,
    is_authenticated: true,
    university_id: "623021038-1",
};
const skillgroupTable = [{"id": 8, "name": "\u0e01\u0e25\u0e38\u0e48\u0e21 A", "info": "", "skills": [{"skill_id_fk": 1, "goal_point": 4.0}, {"skill_id_fk": 2, "goal_point": 5.0}, {"skill_id_fk": 3, "goal_point": 4.0}]}, {"id": 9, "name": "\u0e01\u0e25\u0e38\u0e48\u0e21 B", "info": "", "skills": [{"skill_id_fk": 5, "goal_point": 6.0}, {"skill_id_fk": 6, "goal_point": 3.0}, {"skill_id_fk": 7, "goal_point": 5.0}]}]
const curriculums = [{"id": 5, "th_name": "\u0e2b\u0e25\u0e31\u0e01\u0e2a\u0e39\u0e15\u0e23\u0e43\u0e2b\u0e21\u0e48 \u0e2d\u0e23\u0e48\u0e2d\u0e22\u0e01\u0e27\u0e48\u0e32\u0e40\u0e14\u0e34\u0e21", "en_name": "Better curriculum, Better curry!!!", "start_date": "2023-03-21", "end_date": "2023-03-30", "info": "", "attachment_file": null, "skillgroups": [{"id": 8}, {"id": 9}]}, {"id": 8, "th_name": "\u0e2b\u0e25\u0e31\u0e01\u0e2a\u0e39\u0e15\u0e23\u0e25\u0e31\u0e1a", "en_name": "Ford Ranger Mai Greng Jai Cryyy\ud83d\ude2d\ud83d\ude2d", "start_date": "2023-03-07", "end_date": "2023-03-17", "info": "", "attachment_file": null, "skillgroups": [{"id": 9}]}]

const curriculum_formname = "curriculum-formulate-form-1"
const ref_th_name = curriculum_formname + '-' + 'th_name'
const ref_en_name= curriculum_formname + '-' + 'en_name'
const ref_start_date = curriculum_formname + '-' + 'start_date'
const ref_end_date = curriculum_formname + '-' + 'end_date'
const ref_info= curriculum_formname + '-' + 'info'
const ref_attachment_file = curriculum_formname + '-' + 'attachment_file'
const ref_skillgroups = curriculum_formname + '-' + 'skillgroups'

describe("Curriculum", () => {
    it("curriculum-input-field-validation", async () => {
        const wrapper = mount(Curriculum, {
            localVue,
            data() {
                return {
                    curriculum: {},
                    testMode: true, //Block api calls,

                    user: JSON.parse(JSON.stringify(user_staff)),
                    
                    skillgroupTable: JSON.parse(JSON.stringify(skillgroupTable)),
                    curriculums: JSON.parse(JSON.stringify(curriculums)),
                };
            },

        });

        
        //Test th_name 
        let th_name = wrapper.vm.$refs[ref_th_name];

        // Test th_name :required
        wrapper.setData({ curriculum: { th_name: "" } });
        await flushPromises();
        th_name.performValidation();
        await flushPromises();
        // console.log(th_name.validationErrors)
        expect(th_name.validationErrors).toContain("Thai Name is required.");
        
        // Test en_name : <= 50
        wrapper.setData({ curriculum: { th_name: "a".repeat(101) } });
        await flushPromises();
        th_name.performValidation();
        await flushPromises();
        expect(th_name.validationErrors).toContain("Thai Name must be less than or equal to 50 characters long.");
        //end th_name

        // Test en_name :required
        let en_name = wrapper.vm.$refs[ref_en_name];
        wrapper.setData({ curriculum: { en_name: "" } });
        await flushPromises();
        en_name.performValidation();
        await flushPromises();
        expect(en_name.validationErrors).toContain("English Name is required.");
        
        // Test en_name : <= 50
        wrapper.setData({ curriculum: { en_name: "a".repeat(101) } });
        await flushPromises();
        en_name.performValidation();
        await flushPromises();
        expect(en_name.validationErrors).toContain("English Name must be less than or equal to 50 characters long.");

        //end en_name

        // Test start_date
        let start_date = wrapper.vm.$refs[ref_start_date] 
        wrapper.setData({ curriculum: { start_date: "" } });
        await flushPromises();
        start_date.performValidation();
        await flushPromises();
        expect(start_date.validationErrors).toContain("Start Date is required.");
        //end start_date

        // Test start_date
        let end_date = wrapper.vm.$refs[ref_end_date] 
        wrapper.setData({ curriculum: { end_date: "" } });
        await flushPromises();
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain("End Date is required.");

        // Test start_date < end_date
        wrapper.setData({ curriculum: { start_date : "2023-03-21", end_date: "2023-03-21" } });
        await flushPromises();
        end_date.performValidation();
        await flushPromises();
        expect(end_date.validationErrors).toContain("End date must be later than start date.");

        //end start_date

        // Test info
        const info = wrapper.vm.$refs[ref_info];
        //info : || 201 chars
        wrapper.setData({
            curriculum: {
                info: "a".repeat(201),
            },
        });
        await flushPromises();
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors).toContain(
            "Info must be less than or equal to 200 characters long."
        );
        //end info

        //Test : attachment_file
        const attachment_file = wrapper.vm.$refs[ref_attachment_file];

        //attachment_file : maxFileSize
        wrapper.setData({
            curriculum: { attachment_file: { files: [{ file: { size: 2500000 } }] } },
        });
        await flushPromises();
        attachment_file.performValidation();
        await flushPromises();
        expect(attachment_file.validationErrors).toContain(
            "The file size must not exceed 2 mb."
        );
        

    });

    it("curriculum-form-submission", async () => {
        const wrapper = mount(Curriculum, {
            localVue,
            data() {
                return {
                    curriculum: {},
                    testMode: true, //Block api calls,

                    user: JSON.parse(JSON.stringify(user_staff)),
                    
                    skillgroupTable: JSON.parse(JSON.stringify(skillgroupTable)),
                    curriculums: JSON.parse(JSON.stringify(curriculums)),
                };
            }
        });

        await flushPromises()
        
        let valid_data = JSON.parse(JSON.stringify(curriculums[0]))
        
        let invalids = {
            'th_name' : '',
            'en_name' : '',
            'start_date' : '',
            'end_date' : '',
            'info' : 'a'.repeat(201),
            'attachment_file' : { files: [{ file: { size: 2500000 } }] },
            'skillgroups' : null,
        }

        //Test valid data
        wrapper.setData({ curriculum : JSON.parse(JSON.stringify(valid_data)) });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(true);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(true);
        })

        //Test th_name
        let copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['th_name'] = invalids['th_name'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })
        
        //Test en_name
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['en_name'] = invalids['en_name'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        //Test start_date
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['start_date'] = invalids['start_date'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        //Test end_date
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['end_date'] = invalids['end_date'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        //Test info
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['info'] = invalids['info'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        //Test attachment_file
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['attachment_file'] = invalids['attachment_file'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })

        //Test skillgroups
        copied_data = JSON.parse(JSON.stringify(valid_data));
        copied_data['skillgroups'] = invalids['skillgroups'];
        wrapper.setData({ curriculum : copied_data });
        await flushPromises()
        await wrapper.vm.updateClick().then((result) => {
            expect(result).toBe(false);
        })
        await wrapper.vm.createClick().then((result) => {
            expect(result).toBe(false);
        })


    });
});

