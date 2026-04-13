<script setup>
import { inject } from "vue";

const app = inject("stockApp");
</script>

<template>
  <section class="page-grid">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Stock Management</p>
        <h2>Movement control</h2>
      </div>
      <button class="ghost-button" @click="app.loadStocks(1)">Refresh</button>
    </div>

    <div class="toolbar glass-card">
      <input v-model.trim="app.stockFilters.category" placeholder="Search by category" />
      <input v-model.trim="app.stockFilters.manufacturer" placeholder="Search by manufacturer" />
      <input v-model.trim="app.stockFilters.product_name" placeholder="Search by product name" />
      <select v-model="app.stockFilters.sort">
        <option value="stock_id">Stock ID</option>
        <option value="category">Category</option>
        <option value="manufacturer">Manufacturer</option>
      </select>
      <button @click="app.loadStocks(1)">Apply</button>
    </div>

    <div class="workspace-grid">
      <article class="glass-card form-card">
        <div class="card-heading">
          <p class="eyebrow">Stock In</p>
          <h3>{{ app.editing.stockId ? "Update stock record" : "Add stock" }}</h3>
        </div>
        <form class="stack-form" @submit.prevent="app.submitStock">
          <select v-model="app.stockForm.product" required>
            <option disabled value="">Select product</option>
            <option v-for="item in app.products.value" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <input v-model="app.stockForm.qty" type="number" min="0" placeholder="Quantity" required />
          <input v-model="app.stockForm.user" type="number" min="1" placeholder="User ID" required />
          <div class="form-actions">
            <button v-if="app.isAdmin.value" type="submit">
              {{ app.editing.stockId ? "Update" : "Add Stock" }}
            </button>
            <button v-if="app.editing.stockId" type="button" class="ghost-button" @click="app.resetStockForm">
              Cancel
            </button>
          </div>
        </form>

        <div class="card-heading split-top">
          <p class="eyebrow">Stock Out</p>
          <h3>Remove quantity</h3>
        </div>
        <form class="stack-form" @submit.prevent="app.submitStockOut">
          <input v-model="app.stockOutForm.stockId" type="number" min="1" placeholder="Stock ID" required />
          <input v-model="app.stockOutForm.qty" type="number" min="1" placeholder="Qty to remove" required />
          <button v-if="app.isAdmin.value" type="submit">Remove Stock</button>
        </form>
      </article>

      <article class="glass-card data-card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Product</th>
              <th>Category</th>
              <th>Manufacturer</th>
              <th>Qty</th>
              <th>User</th>
              <th v-if="app.isAdmin.value">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in app.stocks.value" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.product.name }}</td>
              <td>{{ item.product.category }}</td>
              <td>{{ item.product.manufacturer }}</td>
              <td>{{ item.qty }}</td>
              <td>{{ item.user.username }}</td>
              <td v-if="app.isAdmin.value" class="actions-cell">
                <button class="mini-button" @click="app.startStockEdit(item)">Edit</button>
                <button class="mini-button danger" @click="app.removeRecord(`/stocks/${item.id}/`, () => app.loadStocks(app.stockFilters.page))">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pager">
          <button :disabled="app.pageInfo.stocks.page <= 1" @click="app.loadStocks(app.pageInfo.stocks.page - 1)">Prev</button>
          <span>{{ app.pageInfo.stocks.page }} / {{ app.pageInfo.stocks.total_pages || 1 }}</span>
          <button :disabled="app.pageInfo.stocks.page >= app.pageInfo.stocks.total_pages" @click="app.loadStocks(app.pageInfo.stocks.page + 1)">Next</button>
        </div>
      </article>
    </div>
  </section>
</template>
