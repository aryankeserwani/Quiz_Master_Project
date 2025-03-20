import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import Dashboard from "../components/Dashboard.vue";
import Admin from "../components/Admin.vue";
import HomeView from "../components/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
    meta: { requiresAuth: false },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const userData = localStorage.getItem("user");

  // Check if route requires auth
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // If no token, redirect to login
      next({ name: "Login" });
    } else if (to.matched.some((record) => record.meta.requiresAdmin)) {
      // If route requires admin, check if user is admin
      const user = userData ? JSON.parse(userData) : { role: null };
      if (user.role !== "Admin") {
        next({ name: "Dashboard" });
      } else {
        next();
      }
    } else {
      next();
    }
  } else {
    // Allow access to non-auth routes
    next();
  }
});

export default router;
