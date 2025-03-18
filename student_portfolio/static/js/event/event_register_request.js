
let eventRegisterRequestComponent = {
    template: '#event-register-request-template',

    data(){
        return{
            user:"",
            staffs:[],
            events:[],

            modalTitle:"",
            addingNewEvent : false,

            event: {
                eventId: 0,
                title: "",
                date: "",
                mainStaffId: "",
                info: "",
                skills: [],
                approved: false,
                used_for_calculation: false,
            },

            skillTable:"",
            skills: [],

            checkboxes :[],

            // PhotoFileName:"anonymous.png",
            // PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        refreshData(){
            this.is_staff = JSON.parse(document.getElementById('is_staff-data').textContent);

            axios.get(variables.API_URL+"eventRegisterRequest")
            .then((response)=>{
                this.events=response.data;
            });

            axios.get(variables.API_URL+"staff")
            .then((response)=>{
                this.staffs=response.data;
            });

            axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
            });


        },
    addClick(){

        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.
        document.getElementById("createButton").disabled = false;

        this.event = this.getEmptyEvent()
        this.checkboxes = []
        // this.DateOfJoining="",
        // this.PhotoFileName="anonymous.png"
    },
    editClick(event){
        this.modalTitle="Edit Event";
        this.addingNewEvent = false

        this.event = event

        this.checkboxes = []
        if (event.approved) this.checkboxes.push('approved')
        if (event.used_for_calculation) this.checkboxes.push('used_for_calculation')

    },
    createClick(){
        responseData=""

        this.event.skills = this.cleanSkills(this.event.skills)
        delete this.event.eventId

        let outDict = {
            event : this.event,
        }

        axios.post(variables.API_URL+"eventRegisterRequest", outDict)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
            responseData = response.data
        });

        // check if successfully added.
        // if responseData =
        // document.getElementById("createButton").disabled = true;

    },
    updateClick(){

        this.event.skills = this.cleanSkills(this.event.skills);

        this.event.approved = this.checkboxes.includes('approved')
        this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.event)) {
            outDict.append(key.toString(), value)
        }
        outDict.set('skills', JSON.stringify(this.event.skills))


        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"event/" + this.event.eventId,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            // this.refreshData();
            alert(response.data);
            window.location.reload();
        })


    },
    deleteClick(eventId){
        if(!confirm("Are you sure?")){
            return;
        }

        //Make a request.
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"event/" + eventId,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            headers : {
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            alert(response.data);
            // window.location.reload();
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
    }

    // imageUpload(event){
    //     let formData=new FormData();
    //     formData.append('file',event.target.files[0]);
    //     axios.post(
    //         variables.API_URL+"employee/savefile",
    //         formData)
    //         .then((response)=>{
    //             this.PhotoFileName=response.data;
    //         });
    // }

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
        }

        return event
    },
    mounted:function(){
        this.refreshData();

        axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            });


    }
}

const app = Vue.createApp({
    components: {'event-register-request-html' : eventRegisterRequestComponent},


})

app.mount('#app')