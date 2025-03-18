let projectComponent = {

    template : '#project-template',

    data(){
        return {
            modalTitle:"",
            addingNewProject:false,

            showApproved:true,
            // showUnapproved:false,
            // showOptions:true,

            staffTable:[],
            user:{},

            project:{},
            projects:[],

            checkboxes:[],

        }
    },

    methods:{
        getEmptyProject(){
            return {
                id:0,
                title:"",
                start_date: (new Date()).toISOString().split('T')[0],
                end_date: (new Date()).toISOString().split('T')[0],

                info:"",

                created_by:"",
                approved:false,
                approved_by:false,
                used_for_calculation:false,

                attachment_link:"",
                attachment_file:"",

                skills: [],
                staffs: [],
            }
        },

        refreshData(){
            axios.get(variables.API_URL + "project").
             then((response)=>{
                this.projects=response.data;
            })
        },

        addClick(){
            console.log(this.projects)
            this.modalTitle="Add Project"
            this.addingNewProject= true // Signal that we are adding new project.

            this.project = this.getEmptyProject()
            this.checkboxes=[]

        },
        createClick(){

            this.project.skills = this.cleanSkills(this.project.skills);

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.project)) {
                outDict.append(key.toString(), value)
            }

            alert(JSON.stringify(outDict, null, 2))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"project",
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
        editClick(project){
            this.modalTitle="Edit project";
            this.addingNewProject = false

            this.project = JSON.parse(JSON.stringify(project))
            this.checkboxes = []

            if (project.approved)
                this.checkboxes.push('approved')
            if (project.used_for_calculation)
                this.checkboxes.push('used_for_calculation')


        },
        updateClick(){
            this.project.skills = this.cleanSkills(this.project.skills);
            this.project.staffs = this.cleanStaffs(this.project.staffs);

            this.project.approved = this.checkboxes.includes('approved')
            this.project.used_for_calculation = this.checkboxes.includes('used_for_calculation')

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.project)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skills', JSON.stringify(this.project.skills))
            outDict.set('staffs', JSON.stringify(this.project.staffs))
            // this.project.skills = before_altered_project.skills

            alert(JSON.stringify(JSON.stringify(this.project.skills), null, 2))
            alert(JSON.stringify(JSON.stringify(this.project.staffs), null, 2))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"project/" + this.project.id,
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
        deleteClick(projectId){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"project/"+ projectId,
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
            this.project.skills.push({
                id: '',
            })
        },
        removeSkillClick(){
            this.project.skills.pop()
        },

        addStaffClick(){
            this.project.staffs.push({
                id: '',
            })
        },
        removeStaffClick(){
            this.project.staffs.pop()
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
            this.project.attachment_file = event.target.files[0]

        },
        prepareData(){
            this.project = this.getEmptyProject()

        }
    },

    created: async function(){
        this.prepareData()
         await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            })

         axios.get(variables.API_URL + "project").
             then((response)=>{
                this.projects=response.data;
            })

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

    }

}

const app = Vue.createApp({

    components:{
        'project-html' : projectComponent,
    }
})

app.mount('#app')