<script setup>
import { computed, onMounted, provide, ref } from "vue";
import LoginPage from "./pages/LoginPage.vue";
import DashboardPage from "./pages/DashboardPage.vue";
import ProductsPage from "./pages/ProductsPage.vue";
import StocksPage from "./pages/StocksPage.vue";
import CategoriesPage from "./pages/CategoriesPage.vue";
import ManufacturersPage from "./pages/ManufacturersPage.vue";
import { useStockApp } from "./useStockApp";

const app = useStockApp();

const routeMap = {
  login: LoginPage,
  dashboard: DashboardPage,
  products: ProductsPage,
  stocks: StocksPage,
  categories: CategoriesPage,
  manufacturers: ManufacturersPage,
};

const navItems = [
  { key: "dashboard", label: "Dashboard", helper: "Snapshot" },
  { key: "products", label: "Products", helper: "Catalog" },
  { key: "stocks", label: "Stocks", helper: "Movement" },
  { key: "categories", label: "Categories", helper: "Grouping" },
  { key: "manufacturers", label: "Manufacturers", helper: "Suppliers" },
];

function readRoute() {
  const raw = window.location.hash.replace(/^#\/?/, "");
  return raw && routeMap[raw] ? raw : app.isAuthenticated.value ? "dashboard" : "login";
}

const currentRoute = ref(readRoute());

function navigate(route) {
  const safeRoute = routeMap[route] ? route : "dashboard";
  currentRoute.value = safeRoute;
  window.location.hash = `/${safeRoute}`;
}

function syncRoute() {
  const nextRoute = readRoute();
  if (!app.isAuthenticated.value && nextRoute !== "login") {
    navigate("login");
    return;
  }
  currentRoute.value = nextRoute;
}

const CurrentPage = computed(() => routeMap[currentRoute.value] || LoginPage);
const pageTitle = computed(() => navItems.find((item) => item.key === currentRoute.value)?.label || "Login");

provide("stockApp", app);
provide("navigate", navigate);

onMounted(async () => {
  window.addEventListener("hashchange", syncRoute);
  syncRoute();
  if (app.isAuthenticated.value) {
    app.stockForm.user = app.currentUser.value?.id || "";
    await app.loadDashboard();
  }
});
</script>

<template>
  <div :class="['app-shell', { 'app-shell--auth': app.isAuthenticated.value, 'app-shell--guest': !app.isAuthenticated.value }]">
    <div class="ambient ambient-a"></div>
    <div class="ambient ambient-b"></div>

    <template v-if="!app.isAuthenticated.value">
      <CurrentPage />
    </template>

    <template v-else>
      <aside class="sidebar glass-card">
        <div class="brand-block">
          <p class="eyebrow">Stock Suite</p>
          <h1>Control</h1>
        </div>

        <nav class="sidebar-nav">
          <button
            v-for="item in navItems"
            :key="item.key"
            :class="['sidebar-link', { active: currentRoute === item.key }]"
            @click="navigate(item.key)"
          >
            <span>{{ item.label }}</span>
            <small>{{ item.helper }}</small>
          </button>
        </nav>

        <div class="profile-card">
          <strong>{{ app.currentUser.value.username }}</strong>
          <span>{{ app.currentUser.value.role }}</span>
          <button class="ghost-button" @click="app.logout(() => navigate('login'))">Logout</button>
        </div>
      </aside>

      <main class="content-shell">
        <header class="top-strip glass-card">
          <div>
            <p class="eyebrow">Multi Page Control</p>
            <h2>{{ pageTitle }}</h2>
          </div>
          <div v-if="app.globalMessage.text" :class="['banner', app.globalMessage.type]">
            {{ app.globalMessage.text }}
          </div>
        </header>

        <section class="page-shell">
          <CurrentPage />
        </section>
      </main>
    </template>
  </div>
</template>
