<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          placeholder="Enter your username"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          placeholder="Enter your password"
        />
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? "Loading..." : "Login" }}
      </button>

      <div class="register-link">
        Don't have an account?
        <a href="#" @click.prevent="goToRegister">Register</a>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: "",
      isLoading: false,
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.error = "";

      try {
        const response = await this.$http.post("/login", {
          username: this.username,
          password: this.password,
        });

        // Save user data and token to localStorage
        localStorage.setItem("token", response.data.token);
        localStorage.setItem(
          "user",
          JSON.stringify({
            id: response.data.id,
            username: response.data.username,
            email: response.data.email,
            role: response.data.role,
          })
        );

        // Redirect based on role
        if (response.data.role === "Admin") {
          this.$router.push("/admin");
        } else {
          this.$router.push("/dashboard");
        }
      } catch (error) {
        console.error("Login error:", error);
        this.error =
          error.response?.data?.message || "Failed to login. Please try again.";
      } finally {
        this.isLoading = false;
      }
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
.login-container {
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

.register-link {
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
