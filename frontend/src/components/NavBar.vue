<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/">Quiz Master</router-link>
    </div>

    <div class="navbar-menu">
      <template v-if="isLoggedIn">
        <router-link to="/dashboard" v-if="userRole !== 'Admin'"
          >Dashboard</router-link
        >
        <router-link to="/admin" v-if="userRole === 'Admin'"
          >Admin Panel</router-link
        >
        <a href="#" @click.prevent="logout">Logout</a>
      </template>
      <template v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </template>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      userRole: null,
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("token");
    },
  },
  created() {
    // Get user role from localStorage if available
    const userData = localStorage.getItem("user");
    if (userData) {
      const user = JSON.parse(userData);
      this.userRole = user.role;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand a {
  font-size: 1.3rem;
  font-weight: bold;
  color: #42b983;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  gap: 20px;
}

.navbar-menu a {
  color: #2c3e50;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-menu a:hover {
  background-color: #e9ecef;
}

.router-link-exact-active {
  color: #42b983 !important;
  font-weight: bold;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 10px;
  }

  .navbar-brand {
    margin-bottom: 10px;
  }

  .navbar-menu {
    width: 100%;
    justify-content: center;
  }
}
</style>
