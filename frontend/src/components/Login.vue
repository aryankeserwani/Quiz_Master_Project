<template>
  <div :class="['login-root', theme]">
    <div class="login-card">
      <div class="login-left">
        <h2>Hello!</h2>
        <p>Sign in to your account</p>
        <form @submit.prevent="login">
          <div class="input-group">
            <span class="icon"><i class="ri-user-3-line"></i></span>
            <input
              type="text"
              id="username"
              v-model="username"
              required
              placeholder="Username"
              autocomplete="username"
            />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-lock-2-line"></i></span>
            <input
              type="password"
              id="password"
              v-model="password"
              required
              placeholder="Password"
              autocomplete="current-password"
            />
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Loading..." : "SIGN IN" }}
          </button>
          <div class="switch-link">
            Don't have an account?
            <a href="#" @click.prevent="goToRegister">Create</a>
          </div>
        </form>
      </div>
      <div class="login-right">
        <h2>Welcome Back!</h2>
        <p>Login and discover new quizzes and fun. Exciting features await!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAxios } from '@/composables/useAxios';

const router = useRouter();
const route = useRoute();
const { post } = useAxios();

const username = ref('');
const password = ref('');
const error = ref(route.query.message || '');
const isLoading = ref(false);
const theme = inject('theme', ref(localStorage.getItem('theme') || 'dark'));

onMounted(() => {
  document.body.setAttribute('data-theme', theme.value);
  // Watch for theme changes from NavBar
  watch(theme, (val) => {
    document.body.setAttribute('data-theme', val);
  });
  // Add Remix Icon CDN for icons
  if (!document.getElementById('remixicon-cdn')) {
    const link = document.createElement('link');
    link.id = 'remixicon-cdn';
    link.href = 'https://cdn.jsdelivr.net/npm/remixicon@3.4.0/fonts/remixicon.css';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }
});

async function login() {
  isLoading.value = true;
  error.value = "";
  try {
    const data = await post("/login", {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem("token", data.token);
    localStorage.setItem(
      "user",
      JSON.stringify({
        id: data.id,
        username: data.username,
        email: data.email,
        role: data.role,
      })
    );
    if (data.role === "Admin") {
      router.push("/admin");
    } else {
      router.push("/dashboard");
    }
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to login. Please try again.";
  } finally {
    isLoading.value = false;
  }
}

function goToRegister() {
  router.push("/register");
}
</script>

<style scoped>
.login-root {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--login-bg);
  transition: background 0.3s;
}
.login-root.dark {
  --login-bg: #10101a;
}
.login-root.light {
  --login-bg: #f7f7fa;
}
.login-card {
  display: flex;
  width: 700px;
  min-height: 400px;
  background: var(--card-bg);
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
  overflow: hidden;
  transition: background 0.3s;
}
.login-root.dark .login-card {
  --card-bg: #181828;
}
.login-root.light .login-card {
  --card-bg: #fff;
}
.login-left, .login-right {
  flex: 1;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.login-left {
  background: transparent;
}
.login-right {
  background: linear-gradient(135deg, #6a3de8 0%, #8a6bff 100%);
  color: #fff;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.login-right h2 {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 10px;
}
.login-right p {
  color: #f3f3ff;
  font-size: 1rem;
  margin-bottom: 30px;
}
.login-left h2 {
  font-size: 2rem;
  margin-bottom: 8px;
  color: #6a3de8;
}
.login-left p {
  color: #888;
  margin-bottom: 24px;
}
.input-group {
  display: flex;
  align-items: center;
  background: var(--input-bg);
  border-radius: 12px;
  margin-bottom: 18px;
  box-shadow: 0 1px 4px rgba(106, 61, 232, 0.04);
  border: 1px solid var(--input-border);
  transition: background 0.3s, border 0.3s;
}
.login-root.dark .input-group {
  --input-bg: #23233a;
  --input-border: #33334d;
}
.login-root.light .input-group {
  --input-bg: #f3f3ff;
  --input-border: #e0e0f0;
}
.input-group .icon {
  padding: 0 12px;
  color: #6a3de8;
  font-size: 1.2rem;
}
.input-group input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 10px;
  font-size: 1rem;
  color: inherit;
  outline: none;
}
button[type="submit"] {
  width: 100%;
  padding: 12px;
  background: linear-gradient(90deg, #6a3de8 0%, #8a6bff 100%);
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 10px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(106, 61, 232, 0.08);
  transition: background 0.2s;
}
button[type="submit"]:hover {
  background: linear-gradient(90deg, #8a6bff 0%, #6a3de8 100%);
}
button[type="submit"]:disabled {
  background: #cccccc;
  color: #fff;
  cursor: not-allowed;
}
.error-message {
  color: #f44336;
  margin: 10px 0 0 0;
  font-size: 0.95rem;
  text-align: left;
}
.switch-link {
  margin-top: 18px;
  text-align: left;
  font-size: 0.98rem;
  color: #888;
}
.switch-link a {
  color: #6a3de8;
  text-decoration: underline;
  margin-left: 4px;
  font-weight: 600;
}
.switch-link a:hover {
  color: #8a6bff;
}
@media (max-width: 800px) {
  .login-card {
    flex-direction: column;
    width: 95vw;
    min-width: 0;
  }
  .login-left, .login-right {
    padding: 32px 16px;
  }
}
</style>
