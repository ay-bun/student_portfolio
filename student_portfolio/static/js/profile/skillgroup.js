let skillgroupComponent = {
    template: '#skillgroup-template',

    data(){
        return {
            skillgroup:{},
            skillgroups:[],

            skills:[],

            addingNewSkillgroup:false,
            modalTitle:"",

        }
    },

    methods: {

        getEmptySkillgroup(){
            return {
                id : 0,
                name : '',
                info : '',
                skills : '',
            }
        },

        refreshData(){
            axios.get(variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillgroups=response.data;
            });
        },

        addClick(){
            this.modalTitle="Add Skillgroup"
            this.addingNewSkillgroup = true // Signal that we are adding a new event -> Create Button.

            this.skillgroup = this.getEmptySkillgroup()

        },

        editClick(skillgroup){
            this.modalTitle="Edit Skillgroup"
            this.addingNewSkillgroup = false

            this.skillgroup = JSON.parse(JSON.stringify(skillgroup))
        },

        createClick(){

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"skillgroup",
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

            this.skillgroup.skills = this.cleanSkills(this.skillgroup.skills)
            // console.log(this.skillgroup.skills)
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skills', JSON.stringify(this.skillgroup.skills))

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"skillgroup/" + this.skillgroup.id,
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

        deleteClick(skillgroup_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"skillgroup/"+ skillgroup_id,
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
            this.skillgroup.skills.push({
                skill_id_fk: '', goal_point : 0
            })
        },
        removeSkillClick(){
            this.skillgroup.skills.pop()
        },

        cleanSkills(list){
            nonEmpty = []
            ids = []
            for (let i=0;i<list.length; ++i) {
                id = list[i]['skill_id_fk']

                if ( id !== '' && !ids.includes(id)){
                    ids.push(list[i].id);
                    nonEmpty.push(list[i])
                }
            }
            return nonEmpty
        },
    },

    created: function(){
        axios.get(variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillgroups=response.data;
            });

        axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skills=response.data;
            });
    },

    mounted:function(){

    },

}

const app = Vue.createApp({
    components: {'skillgroup-html' : skillgroupComponent},

})

app.mount('#app')