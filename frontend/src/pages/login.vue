<script setup lang="ts">
import { ref } from "vue";
import { authStore } from "../features/auth/store";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

async function handleSubmit() {
  errorMessage.value = "";
  isSubmitting.value = true;

  try {
    await authStore.login({
      username: username.value,
      password: password.value,
    });
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : "Login failed";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="username">Username</label>
      <input
        id="username"
        v-model="username"
        type="text"
        required
        autocomplete="username"
      />
    </div>

    <div>
      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        type="password"
        required
        autocomplete="current-password"
      />
    </div>

    <p v-if="errorMessage">{{ errorMessage }}</p>

    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? "Signing in..." : "Sign in" }}
    </button>
  </form>
</template>
