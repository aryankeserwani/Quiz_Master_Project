<template>
  <div class="login-root">
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
              autofocus
            />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-lock-2-line"></i></span>
            <input
              type="password"
              id="password"
              v-model="password"
              @input="validatePassword"
              required
              placeholder="Password"
            />
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Loading..." : "SIGN IN" }}
          </button>
          <div class="switch-link">
            Don't have an account?
            <a href="#" @click.prevent="goToRegister">Create your account</a>
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
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAxios } from '@/composables/useAxios';

const router = useRouter();
const route = useRoute();
const { post } = useAxios();

const username = ref('');
const password = ref('');
const error = ref(route.query.message || '');
const isLoading = ref(false);

// Validate password strength
const validatePassword = () => {
  if (password.value.length < 8) {
    error.value = "Password must be at least 8 characters long.";
  } else {
    error.value = "";
  }
}

async function login() {
  isLoading.value = true;
  error.value = "";
  try {
    const data = await post("/api/login", {
      username: username.value,
      password: password.value,
    });
    const { access_token, user } = data;
    localStorage.setItem("token", access_token);
    localStorage.setItem("user", JSON.stringify(user));
    if (user.role === "Admin") {
      router.push("/admin");
    } else {
      router.push("/user_dashboard");
    }
  } catch (err) {
    console.error(err);
    error.value = err.response.data.message;
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
  background: #000;
}
.login-card {
  display: flex;
  width: 700px;
  min-height: 400px;
  background: rgba(24, 24, 40, 0.98);
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(106, 61, 232, 0.25);
  overflow: hidden;
}
.login-left, .login-right {
  flex: 1;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #fff;
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
  color: #8a6bff;
}
.login-left p {
  color: #bbb;
  margin-bottom: 24px;
}
.input-group {
  display: flex;
  align-items: center;
  background: #23233a;
  border-radius: 12px;
  margin-bottom: 18px;
  box-shadow: 0 1px 4px rgba(106, 61, 232, 0.08);
  border: 1px solid #6a3de8;
}
.input-group .icon {
  padding: 0 12px;
  color: #8a6bff;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
}
.input-group input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 10px;
  font-size: 1rem;
  color: #fff;
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
  box-shadow: 0 2px 8px rgba(106, 61, 232, 0.18);
  transition: background 0.2s;
}
button[type="submit"]:hover {
  background: linear-gradient(90deg, #8a6bff 0%, #6a3de8 100%);
}
button[type="submit"]:disabled {
  background: #33334d;
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
  color: #bbb;
}
.switch-link a {
  color: #8a6bff;
  text-decoration: underline;
  margin-left: 4px;
  font-weight: 600;
}
.switch-link a:hover {
  color: #6a3de8;
}
/* Custom scrollbar */
.login-root::-webkit-scrollbar {
  width: 8px;
  background: rgba(106, 61, 232, 0.1);
  border-radius: 8px;
}
.login-root::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #6a3de8, #8a6bff);
  border-radius: 8px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 8px rgba(106, 61, 232, 0.3);
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
