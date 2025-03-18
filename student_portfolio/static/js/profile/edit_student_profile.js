let studentProfileComponent = {
    template: '#student-profile-template',

    data(){
        return {
            student:{},
            students:[],
            curriculums:[],

            // skillgroupTable:{},

            addingNewStudent:false,
            modalTitle:"",

        }
    },

    methods: {

        getEmptyStudent(){
            return {
                id : 0,
                university_id : '',
                user_id_fk : '',
                firstname : '',
                middlename : '',
                lastname : '',
                faculty_role : '',

                enroll : '',

            }
        },
        refreshData(){
            axios.get(variables.API_URL+"student")
            .then((response)=>{
                this.students=response.data;
            });
        },

        addClick(){
            this.modalTitle="Add Student"
            this.addingNewStudent = true // Signal that we are adding a new event -> Create Button.

            this.student = this.getEmptyStudent()

        },

        editClick(student){
            this.modalTitle="Edit Student"
            this.addingNewStudent = false

            this.student = JSON.parse(JSON.stringify(student))
        },

        createClick(){
            // console.log(this.curriculum)
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.student)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"student",
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

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.student)) {
                outDict.append(key.toString(), value)
            }
            console.log(this.student)
            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"student/" + this.student.id,
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

        addSkillgroupClick(){
            this.curriculum.skillgroups.push({
                id: '',
            })
        },
        removeSkillgroupClick(){
            this.curriculum.skillgroups.pop()
        },

        cleanManyToManyFields(list){
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

    },

    created: function(){
        axios.get(variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });

        axios.get(variables.API_URL+"student")
            .then((response)=>{
                this.students=response.data;
            });
    },

    mounted:function(){
        // console.log(this.students)
    },

}

const app = Vue.createApp({
    components: {'student-profile-html' : studentProfileComponent},

})

app.mount('#app')