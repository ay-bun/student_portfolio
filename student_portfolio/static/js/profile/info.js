const app = Vue.createApp({
    data(){
        return{
            user:{},
        }
    },
    methods: {

    },
    created:async function(){

       await axios.get(variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;
                // console.log('In parent ')
                // console.log(this.user)
            });

    }

})

let chartComponent = {
    template: '#chart-template',

    // props:['user', 'test'],

    data(){
        return{
            staffs:[],
            events:[],
            user:{},

            modalTitle:"",
            addingNewEvent : false,

            // id:0,
            event: {
                eventId:0,
                title:"",
                date:"",
                mainStaffId:"",
                info:"",
                skills: [],
                approved:false,
                used_for_calculation: false,
                attachment_link: "",
                attachment_file: "",
            },


            // is_staff: true,
            skillLabels:[],
            skillTable:[],
            skillFreq:[],
            checkboxes: [],
            // PhotoFileName:"anonymous.png",
            PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        refreshData(){

            // if (this.user.groups.includes('student'))
            // this.reloadCharts()

            this.event = this.getEmptyEvent()

        },
        addClick(){

            this.modalTitle="Add Event"
            this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.
            // document.getElementById("createButton").disabled = false;

            this.event = this.getEmptyEvent()

            this.checkboxes=[]
            // this.DateOfJoining="",
            // this.PhotoFileName="anonymous.png"
        },
        editClick(event){
            this.modalTitle="Edit Event";
            this.addingNewEvent = false

            this.event = event
            this.checkboxes = []


            //Consider create a list of checkbox variables.
            if (event.approved)
                this.checkboxes.push('approved')
            if (event.used_for_calculation)
                this.checkboxes.push('used_for_calculation')

        },
        createClick(){
            let before_altered_event = this.getEmptyEvent()

            this.event.skills = this.cleanSkills(this.event.skills);
            before_altered_event.skills = this.event.skills

            this.event.skills = JSON.stringify(this.event.skills)

            delete this.event['eventId']
            if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' || this.event.attachment_file === '' )
                delete this.event.attachment_file

            let outDict = new FormData();
            console.log(this.event)
            for (const [key, value] of Object.entries(this.event)) {
                // console.log(key, value);
                outDict.append(key.toString(), value)
            }

            alert(JSON.stringify(outDict, null, 2))

            // axios.post(variables.API_URL+"event", outDict,
            //     { headers: {'Content-Type': 'multipart/form-data'}})
            //     .then((response)=>{
            //     this.refreshData();
            //     alert(response.data);
            // });

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"event",
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers : {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.refreshData();
                alert(response.data);
            })


            //if success
            //document.getElementById("createButton").disabled = true;

            this.event.skills = before_altered_event.skills
        },
        updateClick(){
            //Store only altered fiels.
            let before_altered_event = this.getEmptyEvent()

            this.event.skills = this.cleanSkills(this.event.skills);
            before_altered_event.skills = this.event.skills

            this.event.approved = this.checkboxes.includes('approved')
            this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')

            if (!this.user['is_staff']){
                delete this.event['approved']
                delete this.event['used_for_calculation']
            }

            if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' )
                delete this.event.attachment_file


            this.event.skills = JSON.stringify(this.event.skills)
            alert(JSON.stringify(this.event, null, 2))
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outDict.append(key.toString(), value)
            }

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"event/" + this.event.eventId,
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers : {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.refreshData();
                alert(response.data);
            })

            //Assign some values back.
            this.event.skills = before_altered_event.skills
        },
        deleteClick(eventId){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"event/"+ eventId,
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers : {
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.refreshData();
                alert(response.data);
            })

        },
        addSkillClick(){
            this.event.skills.push({
                skillId: '',
            })
        },
        removeSkillClick(){
            this.event.skills.pop()
        },
        cleanSkills(skills){
            //Remove empty or redundant inputs.
            nonEmpty = []
            skillIds = []
            for (i=0;i<skills.length; ++i) {
                id = skills[i]['skillId']

                if ( id !== "" && !skillIds.includes(id)){
                    nonEmpty.push(skills[i]);
                    skillIds.push(id)
                }
            }
            return nonEmpty
        },

        getEmptyEvent(){

            let event= {
                eventId:0,
                title:"",
                date:"",
                mainStaffId:"",
                info:"",
                skills: [],
                approved:false,
                used_for_calculation: false,
                attachment_link: "",
                attachment_file: "",
            }

            return event
        },

        onFileSelected(event){
            this.event.attachment_file = event.target.files[0]

            let label = document.getElementById("attachment_filename");
            label.innerText = this.event.attachment_file.name

        },

        cleanAttachment_file(attachement_file){

        },

        prepareChartData(){
            let skillFreq = {}
            for (let i=0; i<this.skillTable.length; ++i){
                skillFreq[this.skillTable[i].skillId] = 0
            }
            for (let i=0; i < this.events.length; ++i){
                for (let j=0; j < this.events[i].skills.length; ++j){
                    skillFreq[this.events[i].skills[j].skillId] += 1
                }
            }
            let temp_skillFreq = []
            for (let i=0; i < this.skillTable.length; ++i){
                temp_skillFreq.push(skillFreq[this.skillTable[i].skillId])
            }
            this.skillFreq = temp_skillFreq

            let skillLabels = []
            this.skillTable.forEach(function(e) {
                    skillLabels.push(e.title)
                }
            )

            this.skillLabels = skillLabels

        },
        prepareData(){
            this.user['is_staff'] = Object.values(this.user.groups).includes('staff')
            this.user['is_student'] = Object.values(this.user.groups).includes('student')

            this.prepareChartData()

            // console.log(typeof this.user.groups)

            // console.log(this.user)
        },
        reloadCharts(){

            //Process Data
            //Handle the case where the ids of skills do not start with 1.
            let chartContainer = document.getElementById('chart-container')
            if (this.user.is_staff)
                chartContainer.style.visibility = "hidden"

            // let chartInputs = document.getElementById('chart-inputs')
            // if (this.user)

            const ctx = document.getElementById('myChart').getContext('2d');
            const chart_data = {

              labels: this.skillLabels,
              datasets: [{
                label: 'My First Dataset',
                data: this.skillFreq,
                fill: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(255, 99, 132)'
              },
              ]
            };
            const config = {
                type: 'radar',
                data: chart_data,
                options: {
                    // responsive: true,
                    // maintainAspectRatio: false,
                    scales:{
                        r:{
                            max:5,
                            min:0,
                        },
                    },

                    elements: {
                        line: {
                            borderWidth: 3
                        }
                }
              },
            };

            const myChart = new Chart(ctx, config);

        },

    },

    created:async function(){

        await axios.get(variables.API_URL+"skillTable")
        .then((response)=>{
            this.skillTable=response.data;
        });

        await axios.get(variables.API_URL+"user")
            .then((response)=>{
            this.user=response.data;

        });

        await axios.get(variables.API_URL+"event")
            .then((response)=>{
                this.events=response.data;
            });

        await axios.get(variables.API_URL+"staff")
            .then((response)=>{
                this.staffs=response.data;
            });

        // this.prepareData()
        // this.refreshData()

    },

    mounted:function(){

    }
}

app.component('chart-html', chartComponent)


app.mount('#app')



