<template>
    <div>
        <h1 class="text-center">ภาพรวมการจัดกิจกรรม</h1>
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
                    <button @click="queryPrepareReloadCharts();" class="btn btn-primary">Query</button>
                </FormulateForm>
            </div>
        </div>

        <h2 class="text-center" v-if="barChartLoaded">การจัดกิจกรรมของวิทยาลัยการคอมพิวเตอร์</h2>
        <BarChart :loaded="barChartLoaded" :chartData="barChartData" :chartOptions="barChartOption"></BarChart>

        <FormulateForm>
            <multiselect ref="event-formulate-form-1-skills" v-model="curriculum" :hide-selected="true"
                :close-on-select="true" :multiple="false" :options="curriculums" :custom-label="_curriculum_custom_label"
                track-by="id" placeholder="Select..." open-direction="bottom" :disabled="false">
            </multiselect>
            <formulate-input type="button"
                @click="reloadRadarCharts(); querySummaryAndReloadAverageRadarCharts();">Compute</formulate-input>
        </FormulateForm>
        
        <h2 class="text-center" v-if="radarChartsLoaded">การจัดกิจกรรมของหลักสูตร</h2>
        <div v-if="radarChartsLoaded" :key="'skill-radar-charts-' + radarCharstKey">
            <div v-for="(skillgroup, index ) in skillgroupsForRadarCharts">
                <SkillRadarChart :ref="'skill-radar-chart-' + index" :loaded="radarChartsLoaded"
                    :chartData="radarChartsDataList[index]" :chartOptions="radarChartsOptionList[index]"></SkillRadarChart>
            </div>
        </div>

        <h2 class="text-center" v-if="radarChartsLoaded">ทักษะของนักศึกษาโดยเฉลี่ย</h2>
        <!-- <p>Average Radar Charts</p> -->
        <div v-if="avgRadarChartsLoaded" :key="'avg-skill-radar-charts-' + avgRadarChartsKey">
            <div v-for="(skillgroup, index ) in skillgroupsForRadarCharts">
                <SkillRadarChart :loaded="avgRadarChartsLoaded" :chartData="avgRadarChartsDataList[index]"
                    :chartOptions="avgRadarChartsOptionList[index]"></SkillRadarChart>
            </div>
        </div>
    </div>
</template>

<script>
import SkillRadarChart from "/src/components/profile/skillchart/SkillRadarChart.vue";
import { Multiselect } from "vue-multiselect";
import BarChart from "/src/components/event/event-summary/BarChart.vue";
import axios from "axios";


export default {
    components: {
        Multiselect,

        //Custom
        BarChart,
        SkillRadarChart,
    },

    data() {
        return {
            //API Zone
            user: {},
            profile: {}, //Get Curriculum id from enroll.
            curriculums: [],
            skillgroups: [],
            events: [],
            skillTable: [],

            reindexedSkillTable: {},
            curriculum: null,

            // JS editing zone
            modalTitle: "Edit goal points",
            n_groups: 0,
            // max_n_groups:5,

            skillgroupsForRadarCharts: [],
            radarChartsDataList: [],
            radarChartsOptionList: [],
            radarChartsLoaded: false,
            radarCharstKey: 1,
            eventCurriculumSummaryFreq: {},
            avgRadarChartsDataList: [],
            avgRadarChartsOptionList: [],
            avgRadarChartsLoaded: false,
            avgRadarChartsKey: 1,

            skillFreq: [],

            barChartData: {},
            barChartOption: {},
            barChartLoaded: false,
            // barChartKey:1,



            queryParameters: {
                lower_bound_start_datetime: "2024-01-01T00:00:00.000Z",
                upper_bound_start_datetime: "2028-12-01T00:00:00.000Z"
            },


            variables: {
                API_URL: "",
            },
        }
    },

    methods: {
        refreshData() {

        },
        async queryPrepareReloadCharts() {
            await this.queryEvents();
            this.prepareChartData();
            this.reloadBarChart();
            this.reloadRadarCharts();

            if (this.curriculum !== null) {
                await this.getEventCurriculumSummary()
                this.reloadAverageRaderCharts();
            }
            // this.barChartKey += 1;
        },
        async queryEvents() {
            const eventSearchParams = new URLSearchParams([
                ['used_for_calculation', true],
                ['lower_bound_start_datetime', this.queryParameters.lower_bound_start_datetime],
                ['upper_bound_start_datetime', this.queryParameters.upper_bound_start_datetime]]);
            return await axios.get(this.variables.API_URL + "event", { params: eventSearchParams })
                .then((response) => {
                    this.events = response.data;
                    // console.log(this.events)
                });

            if (curriculum !== null) {
                this.getEventCurriculumSummary();
            }
        },
        async getEventCurriculumSummary() {
            const eventSearchParams = new URLSearchParams([
                ['used_for_calculation', true],
                ['lower_bound_start_datetime', this.queryParameters.lower_bound_start_datetime],
                ['upper_bound_start_datetime', this.queryParameters.upper_bound_start_datetime],
                ['curriculum_id', this.curriculum.id],
            ]);
            return await axios.get(this.variables.API_URL + "event/curriculum-summary", { params: eventSearchParams })
                .then((response) => {
                    this.eventCurriculumSummaryFreq = response.data;
                    // console.log(this.events)
                });
        },
        async querySummaryAndReloadAverageRadarCharts() {
            if (this.curriculum !== null) {
                await this.getEventCurriculumSummary()
                this.reloadAverageRaderCharts();
            }
            return
        },
        getEmptyArrayOfArrays(arrayLength) {
            const arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i) {
                arr[i] = []
            }

            return arr
        },

        getEmptyArrayOfDicts(arrayLength) {
            const arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i) {
                arr[i] = {}
            }

            return arr
        },

        prepareChartData() {
            //Initialize skillFreq


            const skillFreq = {}
            for (let i = 0; i < this.skillTable.length; ++i) {
                skillFreq[this.skillTable[i].id] = 0
            }

            for (let i = 0; i < this.events.length; ++i) {
                for (let j = 0; j < this.events[i].skills.length; ++j) {
                    skillFreq[this.events[i].skills[j].id] += 1
                }
            }

            const reindexedSkillTable = {}
            for (let i = 0; i < this.skillTable.length; ++i) {
                reindexedSkillTable[this.skillTable[i].id] = this.skillTable[i]
            }
            this.reindexedSkillTable = reindexedSkillTable


            this.skillFreq = skillFreq

        },

        getCurriculum() {
            const curriculum_id = this.profile.enroll
            let curriculum = ''
            // console.log('curriculumxxxxx')
            for (let i = 0; i < this.curriculums.length; ++i) {
                if (this.curriculums[i].id === curriculum_id) {
                    curriculum = this.curriculums[i]
                    // console.log(this.curriculums[i])
                    break;
                }
            }
            return curriculum
        },

        getSkillgroupsForChartsFromCurriculum(curriculum) {
            const skillgroups_for_charts = []
            for (let i = 0; i < this.skillgroups.length; ++i) {
                for (let j = 0; j < curriculum.skillgroups.length; ++j)
                    if (this.skillgroups[i].id === curriculum.skillgroups[j].id) {
                        skillgroups_for_charts.push(JSON.parse(JSON.stringify(this.skillgroups[i])))
                    }
            }
            return skillgroups_for_charts
        },

        getDataForRadarCharts(skillgroups_for_charts) {
            const n_groups = skillgroups_for_charts.length
            const chart_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const goal_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const skill_label_data = this.getEmptyArrayOfArrays(n_groups)

            for (let i = 0; i < skillgroups_for_charts.length; ++i) {
                for (let j = 0; j < skillgroups_for_charts[i].skills.length; ++j) {

                    const temp_skill_id = skillgroups_for_charts[i].skills[j].skill_id_fk
                    // console.log(temp_skill_id)
                    // console.log(this.skillTable)
                    chart_freq_data[i].push(this.skillFreq[temp_skill_id])
                    goal_freq_data[i].push(skillgroups_for_charts[i].skills[j].goal_point)
                    skill_label_data[i].push(this.reindexedSkillTable[temp_skill_id].title)
                }
            }

            const result_dict = {
                'chart_freq_data': chart_freq_data,
                'goal_freq_data': goal_freq_data,
                'skill_label_data': skill_label_data
            }

            return result_dict
        },
        getDataForAverageRadarCharts(skillgroups_for_charts) {
            const n_groups = skillgroups_for_charts.length
            const chart_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const goal_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const skill_label_data = this.getEmptyArrayOfArrays(n_groups)

            for (let i = 0; i < skillgroups_for_charts.length; ++i) {
                for (let j = 0; j < skillgroups_for_charts[i].skills.length; ++j) {

                    const temp_skill_id = skillgroups_for_charts[i].skills[j].skill_id_fk
                    // console.log(temp_skill_id)
                    // console.log(this.skillTable)
                    chart_freq_data[i].push(this.eventCurriculumSummaryFreq[temp_skill_id])
                    goal_freq_data[i].push(skillgroups_for_charts[i].skills[j].goal_point)
                    skill_label_data[i].push(this.reindexedSkillTable[temp_skill_id].title)
                }
            }

            const result_dict = {
                'chart_freq_data': chart_freq_data,
                'goal_freq_data': goal_freq_data,
                'skill_label_data': skill_label_data
            }

            return result_dict
        },

        getDataForBarChart() {

            // SkillFreq is indexed by id of the skillTable.
            const bar_chart_non_zero_freq_data = []
            const bar_chart_label = []
            for (const [index, value] of Object.entries(this.skillFreq)) {
                if (value !== 0) {
                    bar_chart_non_zero_freq_data.push(value)
                    bar_chart_label.push(this.reindexedSkillTable[index].title)
                }
            }

            const result_dict = {
                'bar_chart_non_zero_freq_data': bar_chart_non_zero_freq_data,
                'bar_chart_label': bar_chart_label,
            }
            return result_dict;

        },
        reloadBarChart() {
            const data_for_chart = this.getDataForBarChart();
            const bar_chart_non_zero_freq_data = data_for_chart['bar_chart_non_zero_freq_data']
            const bar_chart_label = data_for_chart['bar_chart_label']

            const barChartOption = {
                responsive: true,
                maintainAspectRatio: false,
            };

            const barChartData = {}

            barChartData.labels = bar_chart_label
            barChartData.datasets = [
                {
                    label: '',
                    data: bar_chart_non_zero_freq_data,
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    // borderColor: 'rgb(255, 99, 132)',
                    // pointBackgroundColor: 'rgb(255, 99, 132)',
                    // pointBorderColor: '#fff',
                    // pointHoverBackgroundColor: '#fff',
                    // pointHoverBorderColor: 'rgb(255, 99, 132)'
                }
            ]


            this.barChartData = barChartData;
            this.barChartOption = barChartOption;
            this.barChartLoaded = true;

        },
        reloadRadarCharts() {
            if (this.curriculum === null)
                return;

            this.radarChartsLoaded = false;
            this.radarChartsKey += 1;

            const curriculum = this.curriculum;
            // console.log(curriculum)
            const skillgroups_for_charts = this.getSkillgroupsForChartsFromCurriculum(curriculum)
            this.skillgroupsForRadarCharts = skillgroups_for_charts
            // console.log(skillgroups_for_charts)
            const data_for_chart = this.getDataForRadarCharts(skillgroups_for_charts)
            // console.log(data_for_chart)


            const chart_freq_data = data_for_chart['chart_freq_data']
            const goal_freq_data = data_for_chart['goal_freq_data']
            const skill_label_data = data_for_chart['skill_label_data']

            const chartDataList = []
            const chartOptionList = []
            for (let i = 0; i < skillgroups_for_charts.length; ++i) {

                const chart_data = {}
                chart_data.labels = skill_label_data[i]
                chart_data.datasets = [
                    {
                        label: 'My Skills',
                        data: chart_freq_data[i],
                        fill: true,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgb(255, 99, 132)',
                        pointBackgroundColor: 'rgb(255, 99, 132)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(255, 99, 132)'
                    },
                    {
                        label: 'Goal',
                        data: goal_freq_data[i],
                        fill: true,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgb(54, 162, 235)',
                        pointBackgroundColor: 'rgb(54, 162, 235)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(54, 162, 235)'
                    },
                ]


                const option = {
                    responsive: false,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            max: 10,
                            min: 0,
                        },
                    },

                    elements: {
                        line: {
                            borderWidth: 3,

                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: skillgroups_for_charts[i].name
                        }
                    },
                }

                chartDataList.push(chart_data)
                chartOptionList.push(option)
            }

            this.radarChartsDataList = chartDataList
            this.radarChartsOptionList = chartOptionList
            this.radarChartsLoaded = true

        },

        reloadAverageRaderCharts() {
            if (this.curriculum === null)
                return;

            this.avgRadarChartsLoaded = false;
            this.avgRadarChartsKey += 1;

            const curriculum = this.curriculum;
            //Assume this.skillgroupsForRadarCharts computed.
            const skillgroups_for_charts = this.getSkillgroupsForChartsFromCurriculum(curriculum)
            this.skillgroupsForRadarCharts = skillgroups_for_charts

            const data_for_chart = this.getDataForAverageRadarCharts(skillgroups_for_charts)
            const chart_freq_data = data_for_chart['chart_freq_data']
            const goal_freq_data = data_for_chart['goal_freq_data']
            const skill_label_data = data_for_chart['skill_label_data']

            const chartDataList = []
            const chartOptionList = []
            for (let i = 0; i < skillgroups_for_charts.length; ++i) {

                const chart_data = {}
                chart_data.labels = skill_label_data[i]
                chart_data.datasets = [
                    {
                        label: 'My Skills',
                        data: chart_freq_data[i],
                        fill: true,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgb(255, 99, 132)',
                        pointBackgroundColor: 'rgb(255, 99, 132)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(255, 99, 132)'
                    },
                    {
                        label: 'Goal',
                        data: goal_freq_data[i],
                        fill: true,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgb(54, 162, 235)',
                        pointBackgroundColor: 'rgb(54, 162, 235)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(54, 162, 235)'
                    },
                ]


                const option = {
                    responsive: false,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            max: 10,
                            min: 0,
                        },
                    },

                    elements: {
                        line: {
                            borderWidth: 3,

                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: skillgroups_for_charts[i].name
                        }
                    },
                }

                chartDataList.push(chart_data)
                chartOptionList.push(option)
            }

            this.avgRadarChartsDataList = chartDataList
            this.avgRadarChartsOptionList = chartOptionList
            this.avgRadarChartsLoaded = true
        },

        _curriculum_custom_label({ id, th_name }) {
            if (id === "" || id === null || typeof id === 'undefined') {
                return "Select";
            } else if (Object.is(th_name, null) || typeof th_name === "undefined") {
                for (let i = 0; i < this.skillTable.length; ++i) {
                    if (this.curriculumns[i].id === id) {
                        const temp = this.curriculumns[i];
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.th_name}`;
                    }
                }
            }

            return `${id} ${th_name}`;
        },
    },

    created: async function () {

        this.variables.API_URL = this.$API_URL


        await axios.get(this.variables.API_URL + "user")
            .then((response) => {
                this.user = response.data;
            });

        //Return a list of one element.
        await axios.get(this.variables.API_URL + "student")
            .then((response) => {
                this.profile = response.data[0];
                // console.log(this.profile)
            });

        //Consider returning only the curriculum enrolled by the student.
        await axios.get(this.variables.API_URL + "curriculum")
            .then((response) => {
                this.curriculums = response.data;
                // console.log(this.curriculums)
            });

        await axios.get(this.variables.API_URL + "skillgroup")
            .then((response) => {
                this.skillgroups = response.data;
                // console.log(this.skillgroups)
            });

        await axios.get(this.variables.API_URL + "skillTable")
            .then((response) => {
                this.skillTable = response.data;
                // console.log(this.skillTable)
            });


        this.queryPrepareReloadCharts();
        // await this.queryEvents()

        // this.prepareChartData();
        // this.reloadBarChart();

        // this.reloadCharts()


    },

    mounted: async function () {

    },
}
</script>

