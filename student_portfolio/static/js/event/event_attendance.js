let eventAttendanceComponent = {
    template: '#event-attendance-template',

    data(){
        return{
            modalTitle:"",
            addingNewStudent : false,
            addByFileModalActive : true, //To reset the behavior of the modal.

            studentAttendEvent : {},
            event_id:0,


            csv_file : '',
            studentAttendances:[],

            checkboxes:[],
            checkboxFields:['used_for_calculation']
        }
    },

methods:{
    getEmptyEventAttendance(){
            return {
                id:0,
                event_id_fk:'',
                university_id: '',

                firstname:'',
                middlename:'',
                lastname:'',

                user_id_fk:'',
                synced:false,

                used_for_calculation: false,
            }

    },

    refreshData(){
        axios.get(variables.API_URL+"event-attendance/" + this.event_id)
        .then((response)=>{
            this.studentAttendances=response.data;
            // console.log(this.studentAttendances)
        });

    },

    addClick(){
        this.modalTitle="Add Student"
        this.addingNewStudent = true // Signal that we are adding a new student -> Create Button.

        this.studentAttendEvent = this.getEmptyEventAttendance()

    },

    editClick(attendance){
        this.modalTitle="Edit Student";
        this.addingNewStudent = false

        this.studentAttendEvent = attendance
        this.checkboxes = []

        for(let i=0; i < this.checkboxFields.length; ++i){
            if (this.studentAttendEvent[this.checkboxFields[i]])
                this.checkboxes.push(this.checkboxFields[i])
        }

    },
    createClick(){

        for (let i =0 ; i < this.checkboxFields.length; ++i)
            this.studentAttendEvent[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.studentAttendEvent)) {
            outDict.append(key.toString(), value)
        }
        outDict.set('event_id_fk', this.event_id)

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'post',
            url: variables.API_URL+"event-attendance/",
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

        for (let i=0;i<this.checkboxFields.length; ++i)
            this.studentAttendEvent[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.studentAttendEvent)) {
            outDict.append(key.toString(), value)
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"event-attendance/" + this.event_id + '/' + this.studentAttendEvent.id,
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

    deleteClick(attendance_id){
        if(!confirm("Are you sure?")){
            return;
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"event-attendance/"+ this.event_id + '/' + attendance_id,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            headers : {
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            alert(response.data);
        })
    },

    syncByUniversityIdClick(){

        let outDict = {
            'event_id': this.event_id,
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"sync-attendance-by-university-id/"+ this.event_id,
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

    onCSVFileSelected(event){
        this.csv_file = event.target.files[0]

    },
    bulkAddClick(){

        let outDict = {
            'event_id' : this.event_id,
            'csv_file' : this.csv_file,
        }

        let outForm = new FormData();
        for (const [key, value] of Object.entries(outDict)) {
            outForm.append(key.toString(), value)
        }
        // outForm.set('event_id_fk', this.event_id)

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'post',
            url: variables.API_URL+"event-attendance-bulk-add",
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outForm,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            // console.log(response.data)
            // console.log(response.data.message)
            alert(response.data);
            // alert(response.message);

            //Reset the behavior of the modal.
            this.addByFileModalActive=false
            this.addByFileModalActive=true

        }).catch((error)=>{
            this.refreshData();
            console.log(error.response.data.message)
            console.log(error.response.data.invalid_rows)
            alert(error.response.data.invalid_rows)
            // alert(response.message)
            // alert(response.invalid_rows)
            // alert(response.message)
            ;}
        )
    }

    },

created: function(){


},

mounted:function(){

    this.event_id = JSON.parse(document.getElementById('event_id-data').textContent);
    // console.log(this.event_id)
    this.refreshData()


},

}

const app = Vue.createApp({
    components: {'event-attendance-html' : eventAttendanceComponent},

})

app.mount('#app')