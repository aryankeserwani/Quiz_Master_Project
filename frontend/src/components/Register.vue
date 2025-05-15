<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          required
          placeholder="Enter a username"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          required
          placeholder="Enter a password"
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="formData.email"
          required
          placeholder="Enter your email"
        />
      </div>

      <div class="form-group">
        <label for="fullname">Full Name</label>
        <input
          type="text"
          id="fullname"
          v-model="formData.fullname"
          required
          placeholder="Enter your full name"
        />
      </div>

      <div class="form-group">
        <label for="qualification">Qualification</label>
        <input
          type="text"
          id="qualification"
          v-model="formData.qualification"
          required
          placeholder="Enter your qualification"
        />
      </div>

      <div class="form-group">
        <label for="dob">Date of Birth</label>
        <input type="date" id="dob" v-model="formData.dob" required />
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? "Registering..." : "Register" }}
      </button>

      <div class="login-link">
        Already have an account?
        <a href="#" @click.prevent="goToLogin">Login</a>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAxios } from '@/composables/useAxios';

const router = useRouter();
const { post, loading, error: apiError } = useAxios();

const formData = reactive({
  username: "",
  password: "",
  email: "",
  fullname: "",
  qualification: "",
  dob: ""
});

const isLoading = ref(false);
const error = ref("");
const success = ref("");

async function register() {
  isLoading.value = true;
  error.value = "";
  success.value = "";

  try {
    const data = await post("/register", formData);

    success.value = data.message || "Registration successful!";

    // Clear form after successful registration
    Object.keys(formData).forEach(key => {
      formData[key] = "";
    });

    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (err) {
    console.error("Registration error:", err);
    error.value =
      err.response?.data?.message ||
      "Registration failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
}

function goToLogin() {
  router.push("/login");
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover {
  background-color: #3aa876;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  margin: 10px 0;
}

.success-message {
  color: #4caf50;
  margin: 10px 0;
}

.login-link {
  margin-top: 15px;
  text-align: center;
}

a {
  color: #42b983;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
