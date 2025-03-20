<template>
  <div class="dashboard-container">
    <h1>User Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="user-info">
      <h2>Welcome, {{ user.username }}!</h2>
      <div class="info-card">
        <h3>Your Information</h3>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      user: {},
      loading: true,
    };
  },
  created() {
    this.checkAuth();
    this.loadUserData();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push("/login");
      }
    },
    async loadUserData() {
      try {
        // First try to get user from localStorage
        const userData = localStorage.getItem("user");
        if (userData) {
          this.user = JSON.parse(userData);
          this.loading = false;
        }

        // Also fetch fresh data from the API
        const response = await this.$http.get("/user_dashboard");
        // Update user data with the latest from the server
        this.user = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error loading user data:", error);
        if (error.response && error.response.status === 401) {
          // Unauthorized, token might be expired
          this.logout();
        }
        this.loading = false;
      }
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  margin-top: 50px;
  font-size: 18px;
}

.user-info {
  margin-top: 20px;
}

.info-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logout-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.logout-btn:hover {
  background-color: #d32f2f;
}
</style>
