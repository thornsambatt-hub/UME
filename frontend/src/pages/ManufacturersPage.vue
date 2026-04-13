<script setup>
import { inject } from "vue";

const app = inject("stockApp");
</script>

<template>
  <section class="page-grid">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Manufacturer Management</p>
        <h2>Supplier records</h2>
      </div>
      <button class="ghost-button" @click="app.loadManufacturers(1)">Refresh</button>
    </div>

    <div class="workspace-grid slim">
      <article class="glass-card form-card">
        <div class="card-heading">
          <p class="eyebrow">Editor</p>
          <h3>{{ app.editing.manufacturerId ? "Update manufacturer" : "Create manufacturer" }}</h3>
        </div>
        <form class="stack-form" @submit.prevent="app.submitManufacturer">
          <input v-model.trim="app.manufacturerForm.name" placeholder="Manufacturer name" required />
          <textarea v-model.trim="app.manufacturerForm.description" placeholder="Description" rows="3"></textarea>
          <input v-model.trim="app.manufacturerForm.address" placeholder="Address" />
          <input v-model.trim="app.manufacturerForm.license" placeholder="License" />
          <div class="form-actions">
            <button v-if="app.isAdmin.value" type="submit">
              {{ app.editing.manufacturerId ? "Update" : "Create" }}
            </button>
            <button v-if="app.editing.manufacturerId" type="button" class="ghost-button" @click="app.resetManufacturerForm">
              Cancel
            </button>
          </div>
        </form>
      </article>

      <article class="glass-card list-card">
        <div v-for="item in app.manufacturers.value" :key="item.id" class="list-row">
          <div>
            <strong>#{{ item.id }} {{ item.name }}</strong>
            <p>{{ item.address || item.license || "No extra details" }}</p>
          </div>
          <div v-if="app.isAdmin.value" class="list-actions">
            <button class="mini-button" @click="app.startManufacturerEdit(item)">Edit</button>
            <button class="mini-button danger" @click="app.removeRecord(`/manufacturers/${item.id}/`, () => app.loadManufacturers(app.pageInfo.manufacturers.page))">
              Delete
            </button>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
