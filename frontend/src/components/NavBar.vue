<template>
  <nav :class="['navbar', theme]">
    <div class="nav-brand">
      <router-link to="/">Quiz Master</router-link>
    </div>

    <div class="nav-menu">
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
      <button
        class="theme-toggle"
        @click="toggleTheme"
        :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
      >
        <span v-if="theme === 'dark'">🌞</span>
        <span v-else>🌙</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userRole = ref(null);
const theme = ref(localStorage.getItem('theme') || 'dark');

// Provide theme to all child components
provide('theme', theme);

const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token");
});

onMounted(() => {
  // Get user role from localStorage if available
  const userData = localStorage.getItem("user");
  if (userData) {
    const user = JSON.parse(userData);
    userRole.value = user.role;
  }
  document.body.setAttribute('data-theme', theme.value);
});

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  document.body.setAttribute('data-theme', theme.value);
  localStorage.setItem('theme', theme.value);
}

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
  background-color: var(--navbar-bg);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background 0.3s;
}

.navbar.light {
  --navbar-bg: #f8f9fa;
}

.navbar.dark {
  --navbar-bg: #181828;
}

.nav-brand a {
  font-size: 1.3rem;
  font-weight: bold;
  color: #8a2be2; /* purple */
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-menu a,
.nav-menu .router-link-exact-active {
  color: #8a2be2; /* purple for all links */
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-menu a:hover {
  background-color: #e9ecef;
}

.navbar.dark .nav-menu a:hover {
  background-color: #23233a;
}

.router-link-exact-active {
  color: #6a3de8 !important;
  font-weight: bold;
}

.theme-toggle {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  margin-left: 10px;
  color: #8a2be2;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 10px;
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
