<script setup>
import { inject } from "vue";

const app = inject("stockApp");
const navigate = inject("navigate");

function handleLogin() {
  app.login(() => navigate("dashboard"));
}
</script>

<template>
  <section class="login-layout">
  

    <form class="auth-card glass-card" @submit.prevent="handleLogin">
      <div class="card-heading">
        <p class="eyebrow">Sign In</p>
        <h2>Access the control room</h2>
      </div>
      <label class="field">
        <span>Username</span>
        <input v-model.trim="app.loginForm.username" type="text" required />
      </label>
      <label class="field">
        <span>Password</span>
        <input v-model="app.loginForm.password" type="password" required />
      </label>
      <button type="submit" :disabled="app.isLoading.value">
        {{ app.isLoading.value ? "Checking..." : "Login" }}
      </button>
      <p v-if="app.authError.value" class="error-copy">{{ app.authError.value }}</p>
    </form>
  </section>
</template>
