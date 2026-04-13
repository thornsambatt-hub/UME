<script setup>
import { inject } from "vue";

const app = inject("stockApp");
const navigate = inject("navigate");
</script>

<template>
  <section class="page-grid">
    <div class="hero-panel glass-card">
      <p class="eyebrow">Overview</p>
      <h2>Inventory status at a glance</h2>
      <p class="lead compact">
        Use the sidebar to move between dedicated pages. The dashboard is now a true
        landing page instead of one overloaded screen.
      </p>
      <div class="stat-grid">
        <article v-for="item in app.stats.value" :key="item.label" :class="['stat-card', item.tone]">
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
        </article>
      </div>
    </div>

    <div class="shortcut-grid">
      <button class="nav-card glass-card" @click="navigate('products')">
        <span>Products</span>
        <strong>Search, sort, and maintain catalog items</strong>
      </button>
      <button class="nav-card glass-card" @click="navigate('stocks')">
        <span>Stocks</span>
        <strong>Run stock-in, stock-out, and edits from one screen</strong>
      </button>
      <button class="nav-card glass-card" @click="navigate('categories')">
        <span>Categories</span>
        <strong>Organize product groupings with CRUD forms</strong>
      </button>
      <button class="nav-card glass-card" @click="navigate('manufacturers')">
        <span>Manufacturers</span>
        <strong>Track supplier records in sorted order</strong>
      </button>
    </div>
  </section>
</template>
