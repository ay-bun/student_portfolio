// const horizontalNavbarApp = Vue.createApp({
const horizontalNavbarApp = new Vue({
    el : '#horizontal-navbar',
    data(){
        return {
            user: {},

        }
    },

    created: function(){
        axios.get(variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;

            });

    },

    mounted:function(){

    },
})

// horizontalNavbarApp.mount('#horizontal-navbar')