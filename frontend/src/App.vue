<script setup lang="ts">
import { authStore } from "./features/auth/store";
import Login from "./pages/login.vue";
import ItemsPage from "./pages/items.vue";
</script>

<template>
  <Login v-if="!authStore.state.isAuthenticated" />
  <ItemsPage v-else />
</template>
