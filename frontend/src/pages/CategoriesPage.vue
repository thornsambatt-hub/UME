<script setup>
import { inject } from "vue";

const app = inject("stockApp");
</script>

<template>
  <section class="page-grid">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Category Management</p>
        <h2>Grouping rules</h2>
      </div>
      <button class="ghost-button" @click="app.loadCategories(1)">Refresh</button>
    </div>

    <div class="workspace-grid slim">
      <article class="glass-card form-card">
        <div class="card-heading">
          <p class="eyebrow">Editor</p>
          <h3>{{ app.editing.categoryId ? "Update category" : "Create category" }}</h3>
        </div>
        <form class="stack-form" @submit.prevent="app.submitCategory">
          <input v-model.trim="app.categoryForm.name" placeholder="Category name" required />
          <textarea v-model.trim="app.categoryForm.description" placeholder="Description" rows="5"></textarea>
          <div class="form-actions">
            <button v-if="app.isAdmin.value" type="submit">
              {{ app.editing.categoryId ? "Update" : "Create" }}
            </button>
            <button v-if="app.editing.categoryId" type="button" class="ghost-button" @click="app.resetCategoryForm">
              Cancel
            </button>
          </div>
        </form>
      </article>

      <article class="glass-card list-card">
        <div v-for="item in app.categories.value" :key="item.id" class="list-row">
          <div>
            <strong>#{{ item.id }} {{ item.name }}</strong>
            <p>{{ item.description || "No description" }}</p>
          </div>
          <div v-if="app.isAdmin.value" class="list-actions">
            <button class="mini-button" @click="app.startCategoryEdit(item)">Edit</button>
            <button class="mini-button danger" @click="app.removeRecord(`/categories/${item.id}/`, () => app.loadCategories(app.pageInfo.categories.page))">
              Delete
            </button>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
