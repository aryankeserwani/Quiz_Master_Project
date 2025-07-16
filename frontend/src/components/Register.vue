<template>
  <div :class="['login-root', theme]">
    <div class="login-card">
      <div class="login-left">
        <h2>Hello, friend!</h2>
        <p>Create your account</p>
        <form @submit.prevent="register">
          <div class="input-group">
            <span class="icon"><i class="ri-user-3-line"></i></span>
            <input type="text" v-model="formData.username" required placeholder="Username" />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-lock-2-line"></i></span>
            <input type="password" v-model="formData.password" required placeholder="Password" />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-mail-line"></i></span>
            <input type="email" v-model="formData.email" required placeholder="Email" />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-user-2-line"></i></span>
            <input type="text" v-model="formData.fullname" required placeholder="Full Name" />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-graduation-cap-line"></i></span>
            <input type="text" v-model="formData.qualification" required placeholder="Qualification" />
          </div>
          <div class="input-group">
            <span class="icon"><i class="ri-calendar-line"></i></span>
            <input type="date" v-model="formData.dob" required placeholder="Date of Birth" />
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>
          <button type="submit" :disabled="isLoading">
            {{ isLoading ? 'Registering...' : 'CREATE ACCOUNT' }}
          </button>
          <div class="switch-link">
            Already have an account?
            <a href="#" @click.prevent="goToLogin">Sign in</a>
          </div>
        </form>
      </div>
      <div class="login-right">
        <h2>Glad to see you!</h2>
        <p>Learn more about us and connect after signing up. Etiam aliquam elit diam aliquam.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, inject, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAxios } from '@/composables/useAxios';

const router = useRouter();
const { post } = useAxios();

const formData = reactive({
  username: '',
  password: '',
  email: '',
  fullname: '',
  qualification: '',
  dob: ''
});
const isLoading = ref(false);
const error = ref('');
const success = ref('');
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

async function register() {
  isLoading.value = true;
  error.value = '';
  success.value = '';
  try {
    const data = await post('/register', formData);
    success.value = data.message || 'Registration successful!';
    Object.keys(formData).forEach(key => {
      formData[key] = '';
    });
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed. Please try again.';
  } finally {
    isLoading.value = false;
  }
}

function goToLogin() {
  router.push('/login');
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
  width: 820px;
  min-height: 520px;
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
  padding: 48px 36px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
  min-height: 520px;
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
  display: flex;
  align-items: center;
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
.success-message {
  color: #4caf50;
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
@media (max-width: 900px) {
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
