
let eventComponent = {
    template: '#event-template',

    data(){
        return{

            events:[],
            user:{},

            modalTitle:"",
            addingNewEvent : false,
            showApproved: true,

            event: {},

            skillTable:[],
            staffTable:[],
            checkboxes: [],
            checkboxFields : ['approved', 'used_for_calculation', 'arranged_inside'],

        }
    },

    methods:{
        getEmptyEvent(){
            return {
                id:0,
                title:"",
                start_datetime: (new Date()).toLocaleString(),
                end_datetime: (new Date()).toLocaleString(),
                info:"",

                created_by:"",
                approved:false,
                approved_by:"",
                used_for_calculation: false,
                arranged_inside: false,
                attachment_link: "",
                attachment_file: "",

                //Additional data.
                skills: [],
                staffs: [],
            }
        },
        refreshData(){
            axios.get(variables.API_URL+"event")
            .then((response)=>{
                this.events=response.data;
            });

            this.event=this.getEmptyEvent()
            this.checkboxes = []
        },

    addClick(){
        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.

        this.event = this.getEmptyEvent()
        this.checkboxes=[]
    },

    editClick(event){

        this.modalTitle="Edit Event";
        this.addingNewEvent = false

        this.event = JSON.parse(JSON.stringify(event))
        this.checkboxes = []

        for(let i=0; i<this.checkboxFields.length; ++i){
            if (this.event[this.checkboxFields[i]])
                this.checkboxes.push(this.checkboxFields[i])
        }

    },

    createClick(){

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.event)) {
            outDict.append(key.toString(), value)
        }

        // alert(JSON.stringify(outDict, null, 2))

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'post',
            url: variables.API_URL+"event",
            xsrfCookieName: 'csrftoken',
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
    },
    updateClick(){

        this.event.skills = this.cleanSkills(this.event.skills)
        this.event.staffs = this.cleanStaffs(this.event.staffs)

        for (let i=0;i<this.checkboxFields.length; ++i)
            this.event[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.event)) {
            outDict.append(key.toString(), value)
        }
        outDict.set('skills', JSON.stringify(this.event.skills))
        outDict.set('staffs', JSON.stringify(this.event.staffs))

        //Make a request.
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"event/" + this.event.id,
            xsrfCookieName: 'csrftoken',
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

    },
    deleteClick(event_id){
        if(!confirm("Are you sure?")){
            return;
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"event/"+ event_id,
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
            id: '',
        })
    },
    removeSkillClick(){
        this.event.skills.pop()
    },

    addStaffClick(){
        this.event.staffs.push({
            id: '',
        })
    },
    removeStaffClick(){
        this.event.staffs.pop()
    },

    cleanSkills(list){
        //Remove empty or redundant inputs.
        nonEmpty = []
        ids = []
        for (let i=0;i<list.length; ++i) {
            id = list[i]['id']

            if ( id !== '' && !ids.includes(id)){
                ids.push(list[i].id);
                nonEmpty.push(list[i])
            }
        }
        return nonEmpty
    },
    cleanStaffs(list){
        nonEmpty = []
        ids = []
        for (let i=0;i<list.length; ++i) {
            id = list[i]['id']

            if ( id !== '' && !ids.includes(id)){
                ids.push(list[i].id);
                nonEmpty.push(list[i])
            }
        }
        return nonEmpty
    },
    onFileSelected(event){
        this.event.attachment_file = event.target.files[0]

        // let label = document.getElementById("attachment_filename");
        // label.innerText = this.event.attachment_file.name

    },
    openNewWindow(url){
            window.open(url);
    },

    },

    created:async function(){
        await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            });

        axios.get(variables.API_URL+"event")
            .then((response)=>{
                this.events=response.data;
            });

        axios.get(variables.API_URL+"staff")
        .then((response)=>{
            this.staffTable=response.data;
        });

        axios.get(variables.API_URL+"skillTable")
        .then((response)=>{
            this.skillTable=response.data;
        });

    },

    mounted:function(){
        this.event = this.getEmptyEvent()

    }
}

const app = Vue.createApp({
    components: {'event-html' : eventComponent},

})

app.mount('#app')