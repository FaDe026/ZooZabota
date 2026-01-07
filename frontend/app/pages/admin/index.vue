<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})
import { onMounted, ref } from 'vue'
import { apiFetch } from '~/composables/useAPI' 

interface StatsResponse {
  new_requests_count: number;
  total_dogs_count: number;
}

const checkAuth = () => {
  const token = localStorage.getItem('access_token')
  return !!token 
}

const stats = ref<StatsResponse>({
  new_requests_count: 0,
  total_dogs_count: 0
})

const loading = ref(true)
const error = ref<string | null>(null)

const fetchStats = async () => {
  try {
    loading.value = true
    error.value = null
    
    const data = await apiFetch<StatsResponse>('/stats', {
      method: 'GET'
    })
    
    stats.value = data
  } catch (err) {
    console.error('Error fetching stats:', err)
    error.value = 'Не удалось загрузить статистику'
    stats.value = {
      new_requests_count: 0,
      total_dogs_count: 0
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!checkAuth()) {
    navigateTo('/admin/login')
    return
  }
  
  await fetchStats()
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
        <template v-if="loading">
          <span class="animate-pulse bg-gray-200 h-6 w-48 rounded"></span>
          <span class="animate-pulse bg-gray-200 h-6 w-48 rounded"></span>
        </template>
        <template v-else-if="error">
          <span class="text-red-500">{{ error }}</span>
          <span>Новые заявки: 0</span>
          <span>Животные в приюте: 0</span>
        </template>
        <template v-else>
          <span>Новые заявки: {{ stats.new_requests_count }}</span>
          <span>Животные в приюте: {{ stats.total_dogs_count }}</span>
        </template>
      </div>
      <div class="flex flex-col gap-3">
        <NuxtLink href="/admin/application" class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl transition-transform active:scale-95 md:hover:-translate-y-1">
          Заявки
        </NuxtLink>
        <NuxtLink href="/admin/pets" class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl 
                 transition-transform active:scale-95 md:hover:-translate-y-1">
          Животные
        </NuxtLink>
        <NuxtLink href="/admin/news" class="card-bg card-shadow py-4 text-center rounded-xl text-xl md:text-2xl transition-transform active:scale-95 md:hover:-translate-y-1">
          Новости
        </NuxtLink>
      </div>
    </div>
    <div class="flex justify-center mt-6">
      <button @click="logout" class="btn w-full py-4 text-xl font-medium md:max-w-xs md:mx-auto">
        Выйти
      </button>
    </div>
  </section>
</template>