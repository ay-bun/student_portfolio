let curriculumStudentComponent = {
    template: '#curriculum-student-template',

    data(){
        return {
            curriculum_id : 0,
            students : [],
            user : {},


            modalTitle : '',
            addByFileModalActive : true,

        }
    },

    methods: {
        refreshData(){
            axios.get(variables.API_URL+"student",
                { params: { curriculum_id : this.curriculum_id } })
                .then((response)=>{
                    this.students = response.data;
                })

        },

        onCSVFileSelected(event){
            this.csv_file = event.target.files[0]
        },

        bulkAddClick(){

            let outDict = {
                'curriculum_id' : this.curriculum_id,
                'csv_file' : this.csv_file,
            }

            let outForm = new FormData();
            for (const [key, value] of Object.entries(outDict)) {
                outForm.append(key.toString(), value)
            }


            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"curriculum-student-bulk-add",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outForm,
                headers : {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.refreshData();
                alert(response.data);

                //Reset the behavior of the modal.
                this.addByFileModalActive=false
                this.addByFileModalActive=true
            })
        },

    },

    created: function(){

    },

    mounted: function(){
        this.curriculum_id = JSON.parse(document.getElementById('curriculum_id-data').textContent);
        axios.get(variables.API_URL+"student", { params: { curriculum_id : this.curriculum_id } })
            .then((response)=>{
                this.students = response.data;
        });

        console.log(this.curriculum_id)
        console.log(this.students)
    },


}

const app = Vue.createApp({
    components: {'curriculum-student-html' : curriculumStudentComponent},

})

app.mount('#app')