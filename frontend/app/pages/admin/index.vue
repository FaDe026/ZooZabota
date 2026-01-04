<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})
import { onMounted } from 'vue'
const checkAuth = () => {
  const token = localStorage.getItem('access_token')
  return !!token 
}
onMounted(() => {
  if (!checkAuth()) {
    navigateTo('/admin/login')
  }
})
const logout = () => {
  localStorage.removeItem('access_token')
  navigateTo('/admin/login')
}
</script>

<template>
  <section class="min-h-screen md:h-[calc(100vh-200px)] py-8 px-4 flex flex-col">
    <div class="flex flex-col gap-6">
      <div class="flex text-xl flex-col gap-2 text-text-primary">
        <span>Новые заявки: 2</span>
        <span>Животные в приюте: 124</span>
        <span>Требуют внимания: 4</span>
      </div>
      <div class="flex flex-col gap-3">
        <NuxtLink 
          href="/admin/application"
          class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl 
                 transition-transform active:scale-95 md:hover:-translate-y-1">
          Заявки
        </NuxtLink>
        <NuxtLink 
          href="/admin/pets"
          class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl 
                 transition-transform active:scale-95 md:hover:-translate-y-1">
          Животные
        </NuxtLink>
        <a 
          href=""
          class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl 
                 transition-transform active:scale-95 md:hover:-translate-y-1">
          Новости
        </a>
      </div>
    </div>
    <div class="flex justify-center mt-6">
      <button 
        @click="logout" 
        class="btn w-full py-4 text-xl font-medium md:max-w-xs md:mx-auto">
        Выйти
      </button>
    </div>
  </section>
</template>