<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})
import { ref } from "vue"
const username = ref("")
const password = ref("")
const loading = ref(false)
const error = ref("")
onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    navigateTo('/admin')
  }
})

const login = async () => {
  loading.value = true
  error.value = ""

  try {
    const body = new URLSearchParams()
    body.append("username", username.value)
    body.append("password", password.value)
    const response: {
      access_token: string
      token_type: string
    } = await $fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body
    })
    localStorage.setItem("access_token", response.access_token)
    await navigateTo("/admin")
  } catch (e) {
    error.value = "Неверный логин или пароль"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="flex flex-col justify-center items-center px-2 h-[calc(100vh-200px)] w-full">
    <h1 class="text-center text-4xl text-text-primary mb-6">КОВЧЕГ</h1>
    <form
      class="flex flex-col gap-3 w-full max-w-100"
      @submit.prevent="login">
      <TextInput
        v-model="username"
        placeholder="Логин"
        class="input-grad-bg border-0 shadow-lg"/>
      <TextInput
        v-model="password"
        placeholder="Пароль"
        type="password"
        class="input-grad-bg border-0 shadow-lg"/>
      <label class="text-text-secondary flex items-center gap-2 px-4">
        <input type="checkbox" class="checkbox">
        Я не робот (честно)
      </label>
      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? "Вход.." : "Войти" }}
      </button>
      <p v-if="error" class="text-red-500 text-center">
        {{ error }}
      </p>
      <a href="#" class="self-center text-text-secondary">
        Забыли пароль?
      </a>
    </form>
  </section>
</template>
