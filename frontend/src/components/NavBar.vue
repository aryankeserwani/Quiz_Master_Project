<template>
  <nav v-if="!isLoggedIn" class="navbar navbar-expand-lg navbar-dark">
    <div class="nav-brand">
      <router-link to="/">Quiz Master</router-link>
    </div>
    <div class="nav-menu">
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
    </div>
  </nav>
  <nav v-if="isLoggedIn && userRole === 'Admin'" class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">   
      <router-link to="/admin" class="navbar-brand">
        <span class="fw-bold text-white">Welcome, {{ users.username }}!</span>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center me-4">
          <li class="nav-item dropdown ms-5">
            <a class="nav-link d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown" aria-expanded="false">
              <img :src="users.profile_picture" alt="Profile"
                class="img-fluid rounded-circle mx-2" width="50" height="50">
              <div class="dropdown-toggle">
              </div>
            </a>
            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile my-2">
              <li class="dropdown-header">
                <h6>{{ users.username }}</h6>
                <span>{{ users.email }}</span>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" to="/profile">
                  <i class="bi bi-person me-2"></i>
                  <span>My Profile</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" to="/settings">
                  <i class="bi bi-gear me-2"></i>
                  <span>Settings</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button class="dropdown-item d-flex align-items-center" @click="toggleNightMode">
                  <i :class="isNightMode ? 'bi bi-sun-fill me-2' : 'bi bi-moon-fill me-2'"></i>
                  <span>{{ isNightMode ? 'Light Mode' : 'Night Mode' }}</span>
                </button>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button @click.prevent="openConfirmationModal" class="dropdown-item d-flex align-items-center">
                  <i class="bi bi-box-arrow-right me-2"></i>
                  <span>Logout</span>
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useNightModeStore } from '../store/themeChange';
const { isNightMode, toggleNightMode } = useNightModeStore();

const router = useRouter();
const userRole = ref(null);
const users = ref({});  
const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token");
});
const confirmationModal = ref(null);
const openConfirmationModal = () => {
  const modal = document.getElementById('confirmationModal');
  modal.style.display = 'block';
  modal.style.opacity = '1';
  modal.style.transform = 'translateY(0)';
  modal.style.pointerEvents = 'auto';
  modal.style.zIndex = '1000';
}

const closeConfirmationModal = () => {
  confirmationModal.value.style.display = 'none';
  confirmationModal.value.style.opacity = '0';
  confirmationModal.value.style.transform = 'translateY(-10px)';
  confirmationModal.value.style.pointerEvents = 'none';
  confirmationModal.value.style.zIndex = '0';
}

onMounted(() => {
  const userData = localStorage.getItem("user");
  if (userData) {
    const user = JSON.parse(userData);
    userRole.value = user.role;
    users.value = user;
    console.log(users.value);
  }
});

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  router.push("/login");
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #000;
  box-shadow: 0 2px 4px rgba(106, 61, 232, 0.18);
  transition: background 0.3s;
}

.nav-brand a {
  font-size: 1.3rem;
  font-weight: bold;
  color: #8a6bff;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-menu a,
.nav-menu .router-link-exact-active {
  color: #fff;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-menu a:hover {
  background-color: #6a3de8;
  color: #fff;
}

.router-link-exact-active {
  color: #8a6bff !important;
  font-weight: bold;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 10px;
    background-color: #000;
  }

  .nav-brand {
    margin-bottom: 10px;
  }

  .nav-menu {
    width: 100%;
    justify-content: center;
  }
}
</style>
