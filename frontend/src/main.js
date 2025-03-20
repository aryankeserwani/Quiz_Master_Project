import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

Vue.config.productionTip = false;

// Configure Axios to connect with Flask backend
axios.defaults.baseURL = "http://127.0.0.1:5000/api";
axios.defaults.headers.common["Content-Type"] = "application/json";

// Add interceptor to include auth token in requests
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authentication-Token"] = token;
  }
  return config;
});

Vue.prototype.$http = axios;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
