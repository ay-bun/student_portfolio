<template>
    <div>
    </div>
  </template>
  
  <script>
  // import axios from 'axios'
  import { Buffer } from "buffer";
  import axios from "axios";
  
  export default {
    data() {
      return {};
    },
  
    created: function () {
      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios.defaults.withCredentials = true;
  
      axios.get(this.$API_URL + "logout").then((response) => {
        alert(response.data.detail)
        window.location.replace("/home");

      }).catch((error)=>{
        alert(error.response.data.detail);

      })
    },
  
    methods: {
  
    },
  };
  </script>
  