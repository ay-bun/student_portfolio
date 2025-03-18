<template>
  <div>
    <FormulateForm @submit="sendLoginInfoClick" #default="{ hasErrors }">
      <FormulateInput
        ref="formulate-input-username"
        type="text"
        label="Username"
        name="username"
        validation="required"
      ></FormulateInput>
      <FormulateInput
        ref="formulate-input-password"
        type="password"
        label="Password"
        name="password"
        validation="required"
      ></FormulateInput>

      <FormulateInput type="submit" :disabled="hasErrors">
        Login
      </FormulateInput>
    </FormulateForm>
    <!-- <FormulateInput type="submit" @click="seeCookies">
                Login
            </FormulateInput> -->
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

    axios.get(this.$API_URL + "get-csrf").then((response) => {
      // console.log(response, response.headers["x-csrftoken"]);
      // this.$cookies.set("csrftoken", response.headers["x-csrftoken"], "1d");
      // document.cookie = 'x-csrftoken=' + '; expires=Sun, 1 Jan 2023 00:00:00 UTC; path=/'
      // console.log(document.cookie)
    });
  },

  methods: {
    sendLoginInfoClick(data) {
      
      const token = Buffer.from(
        `${data.username}:${data.password}`,
        "utf8"
      ).toString("base64");

      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios.defaults.withCredentials = true;
      axios({
        method: "post",
        url: this.$API_URL + "custom-login",
        xsrfCookieName: "csrftoken",
        xsrfHeaderName: "X-CSRFToken",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": "csrftoken",
          // 'Authorization' : `Basic ${token}`
        },
        data: {
          username_password: JSON.stringify({
            username: data.username,
            password: data.password,
          }),
        },
      }).then((response) => {
        alert(JSON.stringify(response.data));
        // console.log(response.headers.toJSON());
        // console.log(document.cookie);
        window.location.replace("/home");
      }).catch((error)=>{
        alert(JSON.stringify(error.response.data.detail));
      })
    },

  },
};
</script>
