import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// Create Vue 3 app
const app = createApp(App);

// Use router and mount app
app.use(router);
app.mount("#app");
