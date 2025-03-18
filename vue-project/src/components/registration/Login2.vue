<template>
  <div>
    <div v-html="loginHtml"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loginHtml: "",
    };
  },

  created: function () {
    axios.get("http://127.0.0.1:8000/login").then((response) => {
      this.loginHtml = response.data;
    });
  },
};
</script>
