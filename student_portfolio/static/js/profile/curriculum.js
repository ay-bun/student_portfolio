let curriculumComponent = {
    template: '#curriculum-template',

    data(){
        return {
            curriculum:{},
            curriculums:{},


            skillgroupTable:{},

            addingNewCurriculum:false,
            modalTitle:"",

        }
    },

    methods: {

        getEmptyCurriculum(){
            return {
                id : 0,
                th_name : '',
                en_name : '',
                start_date : '',
                end_date : '',
                info : '',
                attachment_file : '',

                skillgroups : [],

            }
        },
        refreshData(){
            axios.get(variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });
        },

        addClick(){
            this.modalTitle="Add Curriculum"
            this.addingNewCurriculum = true // Signal that we are adding a new event -> Create Button.

            this.curriculum = this.getEmptyCurriculum()

        },

        editClick(curriculum){
            this.modalTitle="Edit Curriculum"
            this.addingNewCurriculum = false

            this.curriculum = JSON.parse(JSON.stringify(curriculum))
        },

        createClick(){
            // console.log(this.curriculum)
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"curriculum",
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

            this.curriculum.skillgroups = this.cleanSkillgroups(this.curriculum.skillgroups)
            // console.log(this.curriculum)
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skillgroups', JSON.stringify(this.curriculum.skillgroups))

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"curriculum/" + this.curriculum.id,
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

        deleteClick(curriculum_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"curriculum/"+ curriculum_id,
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

        addSkillgroupClick(){
            this.curriculum.skillgroups.push({
                id: '',
            })
        },
        removeSkillgroupClick(){
            this.curriculum.skillgroups.pop()
        },

        cleanSkillgroups(list){
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
            this.curriculum.attachment_file = event.target.files[0]

            // let label = document.getElementById("attachment_filename");
            // label.innerText = this.event.attachment_file.name

        },
        openNewWindow(url){
            window.open(url);
        },
    },

    created: function(){
        axios.get(variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });

        axios.get(variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillgroupTable=response.data;
            });

    },

    mounted:function(){

    },

}


const app = Vue.createApp({
    components: {'curriculum-html' : curriculumComponent},

})

app.mount('#app')