<script setup>
import { inject } from "vue";

const app = inject("stockApp");
</script>

<template>
  <section class="page-grid">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Product Management</p>
        <h2>Catalog workspace</h2>
      </div>
      <button class="ghost-button" @click="app.loadProducts(1)">Refresh</button>
    </div>

    <div class="toolbar glass-card">
      <input v-model.trim="app.productFilters.id" placeholder="Search by ID" />
      <input v-model.trim="app.productFilters.name" placeholder="Search by name" />
      <input v-model.trim="app.productFilters.category" placeholder="Search by category" />
      <select v-model="app.productFilters.sort">
        <option value="default">Default</option>
        <option value="id_asc">ID ascending</option>
        <option value="price_desc">Price descending</option>
        <option value="manufacturer_asc">Manufacturer ascending</option>
      </select>
      <button @click="app.loadProducts(1)">Apply</button>
    </div>

    <div class="workspace-grid">
      <article class="glass-card form-card">
        <div class="card-heading">
          <p class="eyebrow">Editor</p>
          <h3>{{ app.editing.productId ? "Update product" : "Create product" }}</h3>
        </div>
        <form class="stack-form" @submit.prevent="app.submitProduct">
          <input v-model.trim="app.productForm.name" placeholder="Product name" required />
          <textarea v-model.trim="app.productForm.description" placeholder="Description" rows="3"></textarea>
          <input v-model="app.productForm.price" type="number" step="0.01" min="0" placeholder="Price" required />
          <label class="field">
            <span>Made at</span>
            <input v-model="app.productForm.made_at_date" type="datetime-local" required />
          </label>
          <label class="field">
            <span>Expires at</span>
            <input v-model="app.productForm.expiration_date" type="datetime-local" required />
          </label>
          <select v-model="app.productForm.manufacturer" required>
            <option disabled value="">Select manufacturer</option>
            <option v-for="item in app.manufacturers.value" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <select v-model="app.productForm.category" required>
            <option disabled value="">Select category</option>
            <option v-for="item in app.categories.value" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>
          <div class="form-actions">
            <button v-if="app.isAdmin.value" type="submit">
              {{ app.editing.productId ? "Update" : "Create" }}
            </button>
            <button v-if="app.editing.productId" type="button" class="ghost-button" @click="app.resetProductForm">
              Cancel
            </button>
          </div>
        </form>
      </article>

      <article class="glass-card data-card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Category</th>
              <th>Manufacturer</th>
              <th>Price</th>
              <th v-if="app.isAdmin.value">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in app.products.value" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.category.name }}</td>
              <td>{{ item.manufacturer.name }}</td>
              <td>${{ Number(item.price).toFixed(2) }}</td>
              <td v-if="app.isAdmin.value" class="actions-cell">
                <button class="mini-button" @click="app.startProductEdit(item)">Edit</button>
                <button class="mini-button danger" @click="app.removeRecord(`/products/${item.id}/`, () => app.loadProducts(app.productFilters.page))">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pager">
          <button :disabled="app.pageInfo.products.page <= 1" @click="app.loadProducts(app.pageInfo.products.page - 1)">Prev</button>
          <span>{{ app.pageInfo.products.page }} / {{ app.pageInfo.products.total_pages || 1 }}</span>
          <button :disabled="app.pageInfo.products.page >= app.pageInfo.products.total_pages" @click="app.loadProducts(app.pageInfo.products.page + 1)">Next</button>
        </div>
      </article>
    </div>
  </section>
</template>
