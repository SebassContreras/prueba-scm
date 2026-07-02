<script setup lang="ts">
import { ref } from "vue";
import { searchItems, setItemStatus } from "../features/items/service";
import type { Item, Filter } from "../features/items/types";
import { authStore } from "../features/auth/store";

const items = ref<Item[]>([]);
const isLoading = ref(false);
const errorMessage = ref("");
const updatingId = ref<number | null>(null);
const hasSearched = ref(false);

// Bonus: basic filters over status / warehouse_id
const statusFilter = ref("");
const warehouseFilter = ref("");

function buildFilters(): Filter[] {
  const filters: Filter[] = [];
  if (statusFilter.value) {
    filters.push({
      field: "status",
      operator: "eq",
      value: statusFilter.value,
    });
  }
  if (warehouseFilter.value) {
    filters.push({
      field: "warehouse_id",
      operator: "eq",
      value: Number(warehouseFilter.value),
    });
  }
  return filters;
}

async function handleSearch() {
  isLoading.value = true;
  errorMessage.value = "";
  hasSearched.value = true;

  try {
    items.value = await searchItems(buildFilters());
  } catch (error) {
    // http.ts throws this specific message when the token is missing/expired
    // and the refresh attempt also failed.
    if (error instanceof Error && error.message === "Session expired") {
      authStore.logout();
      return;
    }

    errorMessage.value =
      error instanceof Error
        ? error.message
        : "Something went wrong while loading items";
  } finally {
    isLoading.value = false;
  }
}

async function handleStatusChange(item: Item, newStatus: string) {
  updatingId.value = item.id;
  errorMessage.value = "";

  try {
    const result = await setItemStatus(item.id, newStatus);

    if ("success" in result && result.success === false) {
      errorMessage.value = result.error;
      return;
    }

    const updated = result as Item;
    const index = items.value.findIndex((i) => i.id === updated.id);
    if (index !== -1) items.value[index] = updated;
  } catch (error) {
    if (error instanceof Error && error.message === "Session expired") {
      authStore.logout();
      return;
    }

    errorMessage.value =
      error instanceof Error ? error.message : "Failed to update item status";
  } finally {
    updatingId.value = null;
  }
}

</script>

<template>
  <div>
    <div class="header">
      <h1>Items</h1>
    </div>

    <div class="filters">
      <label>
        Status
        <select v-model="statusFilter">
          <option value="">All</option>
          <option value="pending">pending</option>
          <option value="active">active</option>
          <option value="shipped">shipped</option>
          <option value="cancelled">cancelled</option>
        </select>
      </label>

      <label>
        Warehouse ID
        <input v-model="warehouseFilter" type="number" placeholder="e.g. 3" />
      </label>

      <button type="button" :disabled="isLoading" @click="handleSearch">
        {{ isLoading ? "Searching..." : "Buscar items" }}
      </button>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <p v-if="!hasSearched && !isLoading">
      Click "Buscar items" to load results.
    </p>
    <p
      v-else-if="
        !isLoading && hasSearched && items.length === 0 && !errorMessage
      "
    >
      No items found.
    </p>

    <table v-if="items.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>SKU</th>
          <th>Status</th>
          <th>Warehouse</th>
          <th>Created At</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.sku }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.warehouse_id }}</td>
          <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          <td>
            <select
              :value="item.status"
              :disabled="updatingId === item.id"
              @change="
                handleStatusChange(
                  item,
                  ($event.target as HTMLSelectElement).value,
                )
              "
            >
              <option value="pending">pending</option>
              <option value="active">active</option>
              <option value="shipped">shipped</option>
              <option value="cancelled">cancelled</option>
            </select>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
