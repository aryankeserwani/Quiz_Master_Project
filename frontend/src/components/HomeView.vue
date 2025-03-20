<template>
  <div class="home">
    <div class="hero">
      <h1>Welcome to Quiz Master</h1>
      <p class="subtitle">Test your knowledge and challenge your friends!</p>

      <div class="cta-buttons">
        <router-link to="/login" class="btn btn-primary" v-if="!isLoggedIn"
          >Log In</router-link
        >
        <router-link to="/register" class="btn btn-secondary" v-if="!isLoggedIn"
          >Register</router-link
        >
        <router-link to="/dashboard" class="btn btn-primary" v-if="isLoggedIn"
          >Go to Dashboard</router-link
        >
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <h3>Create Quizzes</h3>
        <p>Design custom quizzes on any topic</p>
      </div>

      <div class="feature-card">
        <h3>Challenge Friends</h3>
        <p>Share your quizzes with friends</p>
      </div>

      <div class="feature-card">
        <h3>Track Progress</h3>
        <p>See your improvement over time</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("token");
    },
  },
};
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  margin-bottom: 40px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 16px;
  color: #2c3e50;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.btn {
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover {
  background-color: #3aa876;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #2c3e50;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background-color: #e9ecef;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.feature-card {
  padding: 30px;
  border-radius: 8px;
  background-color: #f8f9fa;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.feature-card h3 {
  margin-bottom: 10px;
  color: #42b983;
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 15px;
  }

  h1 {
    font-size: 2rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 250px;
    margin-bottom: 10px;
  }
}
</style>
