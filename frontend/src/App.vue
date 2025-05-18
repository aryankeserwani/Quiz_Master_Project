<template>
  <div id="app">
    <NavBar v-if="!isHomePage" />
    <main class="main-content" :class="{ 'home-page': isHomePage }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isHomePage = computed(() => route.path === '/' || route.path === '/home');
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f5f7fa;
  overflow-x: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}

.home-page {
  padding: 0;
  margin: 0;
  width: 100%;
  overflow-x: hidden;
}

a {
  color: #42b983;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
