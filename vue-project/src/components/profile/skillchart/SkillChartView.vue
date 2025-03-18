<template>
    <div>
        <h1 class="text-center">ทักษะของฉัน</h1>
        <h2 class="text-left">{{ curriculum.th_name }}</h2>
        <div v-if="chartsLoaded">
            <div v-for="(skillgroup, index ) in skillgroupsForRadarCharts" :key="'skill-radar-chart-' + index">
                <SkillRadarChart :ref="'skill-radar-chart-' + index"  :loaded="chartsLoaded" :chartData="chartDataList[index]" :chartOptions="chartOptionList[index]"></SkillRadarChart>
            </div>
        </div>
    </div>
</template>

<script>
import SkillRadarChart from "/src/components/profile/skillchart/SkillRadarChart.vue";
import axios from "axios";


export default {
    components:{
        SkillRadarChart,
    },

    data(){
        return{
            //API Zone
            user:{},
            profile:{}, //Get Curriculum id from enroll.
            curriculum : {},
            curriculums:[],
            skillgroups:[],
            skillTable:[],
            events:[],

            reindexedSkillTable:{},

            // JS editing zone
            modalTitle:"Edit goal points",
            n_groups:0,
            max_n_groups:5,

            chartDataList:[],
            chartOptionList:[],
            chartsLoaded:false,
            skillgroupsForRadarCharts:[],

            skillFreq:[],
            // skillLabels:[],

            // radarCharts:[],
            // chartActive:false,
            // checkboxes: [],
            variables: {
                API_URL: "",
            },
        }
    },

    methods:{
        refreshData(){

        },
        getEmptyArrayOfArrays(arrayLength){
            const arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i ){
                arr[i] = []
            }
            
            return arr
        },

        getEmptyArrayOfDicts(arrayLength){
            const arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i ){
                arr[i] = {}
            }

            return arr
        },

        prepareChartData(){
            //Initialize skillFreq


            const skillFreq = {};
            for (let i=0; i<this.skillTable.length; ++i){
                skillFreq[this.skillTable[i].id] = 0
            }

            for (let i=0; i < this.events.length; ++i){
                for (let j=0; j < this.events[i].skills.length; ++j){
                    skillFreq[this.events[i].skills[j].id] += 1
                }
            }

            const reindexedSkillTable = {}
            for (let i=0; i< this.skillTable.length; ++i){
                reindexedSkillTable[this.skillTable[i].id] = this.skillTable[i]
            }
            this.reindexedSkillTable = reindexedSkillTable


            this.skillFreq = skillFreq

        },

        getCurriculum(){
            const curriculum_id = this.profile.enroll
            let curriculum = ''
            // console.log('curriculumxxxxx')
            for (let i = 0; i < this.curriculums.length; ++i){
                if (this.curriculums[i].id === curriculum_id){
                    curriculum = this.curriculums[i]
                    // console.log(this.curriculums[i])
                    break;
                }
            }
            return curriculum
        },

        getSkillgroupsForChartsFromCurriculum(curriculum){
            const skillgroups_for_charts = []
            for(let i = 0; i < this.skillgroups.length; ++i){
                for(let j = 0; j < curriculum.skillgroups.length; ++j)
                    if (this.skillgroups[i].id === curriculum.skillgroups[j].id){
                        skillgroups_for_charts.push(JSON.parse(JSON.stringify(this.skillgroups[i])))
                    }
            }
            return skillgroups_for_charts
        },

        getDataForChart(skillgroups_for_charts){
            const n_groups = skillgroups_for_charts.length
            const chart_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const goal_freq_data = this.getEmptyArrayOfArrays(n_groups)
            const skill_label_data = this.getEmptyArrayOfArrays(n_groups)

            for(let i = 0; i < skillgroups_for_charts.length ; ++i ){
                for (let j = 0; j < skillgroups_for_charts[i].skills.length; ++j){

                    const temp_skill_id = skillgroups_for_charts[i].skills[j].skill_id_fk
                    // console.log(temp_skill_id)
                    // console.log(this.skillTable)
                    chart_freq_data[i].push( this.skillFreq[ temp_skill_id ])
                    goal_freq_data[i].push( skillgroups_for_charts[i].skills[j].goal_point )
                    skill_label_data[i].push(this.reindexedSkillTable[ temp_skill_id ].title)
                }
            }

            const result_dict = {
                'chart_freq_data' :chart_freq_data,
                'goal_freq_data' : goal_freq_data, 
                'skill_label_data' : skill_label_data
            }

            return result_dict
        },

        reloadCharts(){
            
            this.chartsLoaded=false;

            const curriculum = this.getCurriculum()
            this.curriculum = curriculum;
            // console.log(curriculum)
            const skillgroups_for_charts = this.getSkillgroupsForChartsFromCurriculum(curriculum)
            this.skillgroupsForRadarCharts = skillgroups_for_charts;
            // console.log(skillgroups_for_charts)
            const data_for_chart = this.getDataForChart(skillgroups_for_charts)
            // console.log(data_for_chart)
            
            
            const chart_freq_data = data_for_chart['chart_freq_data']
            const goal_freq_data = data_for_chart['goal_freq_data']
            const skill_label_data = data_for_chart['skill_label_data']

            const chartDataList = []
            const chartOptionList = []
            for (let i = 0; i < skillgroups_for_charts.length; ++i ){

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
                    scales:{
                        r:{
                            max:10,
                            min:0,
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
            
            this.chartDataList = chartDataList
            this.chartOptionList = chartOptionList
            this.chartsLoaded = true
        }

    },

    created: async function(){

        this.variables.API_URL = this.$API_URL


        await axios.get(this.variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;
                });

        //Return a list of one element.
        await axios.get(this.variables.API_URL+"student")
                .then((response)=>{
                this.profile=response.data[0];
                // console.log(this.profile)
                });

        //Consider returning only the curriculum enrolled by the student.
        await axios.get(this.variables.API_URL+"curriculum")
                .then((response)=>{
                this.curriculums=response.data;
                // console.log(this.curriculums)
                });

        await axios.get(this.variables.API_URL+"skillgroup")
                .then((response)=>{
                this.skillgroups=response.data;
                // console.log(this.skillgroups)
                });

        await axios.get(this.variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
                // console.log(this.skillTable)
            });

        const eventAttendedParams = new URLSearchParams([['event_used_for_calculation', true], ['event_attendance_used_for_calculation', true]]);
        await axios.get(this.variables.API_URL+"event-attended/list", { params : eventAttendedParams} )
            .then((response)=>{
                this.events=response.data;
                // console.log(this.events)
            });

        this.prepareChartData()
        this.reloadCharts()
    

    },

    mounted: async function(){

    },
}
</script>