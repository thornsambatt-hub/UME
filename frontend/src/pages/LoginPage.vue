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
    <div class="login-copy glass-card">
      <p class="eyebrow">Stock Control Suite</p>
      <h1>Sharper inventory flow, cleaner operator control.</h1>
      <p class="lead">
        Move between pages for products, stock, categories, and manufacturers with a
        modern control panel connected directly to your Django API.
      </p>
      <div class="accent-grid">
        <div>
          <strong>Role Aware</strong>
          <span>Admin and User experiences stay separated.</span>
        </div>
        <div>
          <strong>Search Ready</strong>
          <span>Find products and stock with focused filters.</span>
        </div>
        <div>
          <strong>Live API</strong>
          <span>Runs against your `/api` backend endpoints.</span>
        </div>
      </div>
    </div>

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
