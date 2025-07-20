<template>
  <div class="admin-container">
    <h1>Admin Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="admin-panel">
      
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAxios } from '@/composables/useAxios';

const user = ref({});
const router = useRouter();
const { get, loading: apiLoading } = useAxios();
const loading = ref(true);

onMounted(() => {
  checkAuth();
  loadAdminData();
});

function checkAuth() {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  // Check if user is logged in and has admin role
  if (!token || user.role !== "Admin") {
    router.push("/login");
  }
}

async function loadAdminData() {
  try {
    // Get admin dashboard data
    const data = await get("/api/admin");
    console.log("Admin data:", data);
    user.value = data;
    loading.value = false;
  } catch (error) {
    console.error("Error loading admin data:", error);
    if (error.response && error.response.status === 401) {
      // Unauthorized, token might be expired or user is not admin
      logout();
    }
    loading.value = false;
  }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  router.push("/login");
}
</script>

<style scoped>
.admin-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  margin-top: 50px;
  font-size: 18px;
}

.welcome-section {
  margin-bottom: 30px;
}

.admin-sections {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.admin-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
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
