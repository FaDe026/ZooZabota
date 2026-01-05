<script setup lang="ts">
definePageMeta({ layout: 'default' })

import { ref, computed, watch } from 'vue'
import { apiFetch } from '~/composables/useAPI.ts'

const route = useRoute()
const router = useRouter()
const applicationId = Number(route.params.id)

interface RequestApiResponse {
  id: number
  dog_id: number
  full_name: string
  phone: string
  email: string | null
  status: string
  type: string
  created_at: string
  adoption_request?: Record<string, any> | null
}

interface Application {
  id: number
  petName: string
  clientName: string
  phone: string
  email?: string
  type: 'adoption' | 'custody'
  status: 'pending' | 'in_progress' | 'approved' | 'rejected'
  createdAt: Date
  petId: number
  adoptionDetails?: Record<string, any>
}

const application = ref<Application | null>(null)
const localStatus = ref<Application['status']>('pending')
const isLoading = ref(false)
const errorMessage = ref<string | null>(null)

const { pending } = await useAsyncData(
  `request-${applicationId}`,
  async () => {
    const response = await apiFetch<RequestApiResponse>(`/requests/${applicationId}`)

    let petName = 'Питомец не указан'
    if (response.dog_id) {
      try {
        const dog = await apiFetch<{ name: string }>(`/dogs/${response.dog_id}`)
        petName = dog.name
      } catch {
        petName = `Собака #${response.dog_id}`
      }
    }

    application.value = {
      id: response.id,
      petName,
      clientName: response.full_name,
      phone: response.phone,
      email: response.email ?? undefined,
      type: response.type === 'Усыновление' ? 'adoption' : 'custody',
      status: ({
        'Новая': 'pending',
        'В работе': 'in_progress',
        'Принято': 'approved',
        'Отклонено': 'rejected'
      } as any)[response.status] || 'pending',
      createdAt: new Date(response.created_at),
      petId: response.dog_id,
      adoptionDetails: response.adoption_request ?? undefined
    }

    return true
  }
)

watch(application, val => {
  if (val) localStatus.value = val.status
})


const adoptionFieldLabels: Record<string, string> = {
  family_member_count: 'Семья',
  had_experience_adoption_pet: 'Опыт с питомцами',
  adoption_purpose: 'Цель усыновления',
  housing_type: 'Тип жилья',
  housing_area: 'Площадь жилья'
}

const saveStatus = async () => {
  if (!application.value) return
  
  isLoading.value = true
  errorMessage.value = null
  
  try {
    const statusMapping = {
      pending: 'Новая',
      in_progress: 'В работе',
      approved: 'Завершена', 
      rejected: 'Отклонено'
    }
    
    await apiFetch(`/requests/${applicationId}`, {
    method: 'PATCH',
    body: JSON.stringify({
      status: statusMapping[localStatus.value as keyof typeof statusMapping]
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    
    if (application.value) {
      application.value.status = localStatus.value
    }
    
    alert('Статус успешно обновлен')
    router.push('/admin/application')
    
  } catch (error: any) {
    console.error('Ошибка при сохранении статуса:', error)
    errorMessage.value = 'Не удалось обновить статус заявки'
  } finally {
    isLoading.value = false
  }
}

const goBack = () => router.back()

const handleContact = () => {
  if (!application.value) return
  window.location.href = `tel:${application.value.phone}`
}

const pageTitle = computed(() =>
  application.value?.type === 'adoption'
    ? 'Заявка на усыновление'
    : 'Заявка на опекунство'
)

const getStatusText = (s: Application['status']) => ({
  pending: 'Новая',
  in_progress: 'В работе',
  approved: 'Завершена', 
  rejected: 'Отклонено'
}[s])

const getStatusClass = (s: Application['status']) => ({
  pending: 'text-blue-500 border-blue-500',
  in_progress: 'text-yellow-500 border-yellow-500',
  approved: 'text-green-500 border-green-500',
  rejected: 'text-red-500 border-red-500'
}[s])
</script>

<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <div class="base-container mx-auto relative flex justify-center items-center mb-2">
        <svg 
          class="absolute left-0 cursor-pointer" 
          @click="goBack" 
          width="55" 
          height="47"
          viewBox="0 0 55 47" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg">
          <path 
            d="M43.5416 23.5H11.4583" 
            stroke="#1A3C40" 
            stroke-width="5" 
            stroke-linecap="round"
            stroke-linejoin="round" />
          <path 
            d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" 
            stroke="#1A3C40" 
            stroke-width="5"
            stroke-linecap="round" 
            stroke-linejoin="round" />
        </svg>

        <h1 class="text-2xl text-text-primary text-center font-bold">
          {{ pageTitle }}
        </h1>
      </div>

      <div class="mx-auto base-container p-9 py-3 max-w-3xl">
        <div v-if="pending" class="text-center py-20">
          Загрузка..
        </div>

        <div v-else-if="application" class="base-card rounded-2xl p-8 shadow-xl relative">
          <span
            :class="[
              'absolute top-6 right-6 text-base px-6 py-1 rounded-full border-2',
              getStatusClass(application.status)
            ]">
            {{ getStatusText(application.status) }}
          </span>

          <h2 class="text-2xl text-text-primary mb-8 text-center">
            {{ application.petName }}
          </h2>
          <div class="space-y-1 mb-6 text-lg">
            <p>{{ application.clientName }}</p>
            <p>{{ application.phone }}</p>
            <p v-if="application.email">{{ application.email }}</p>
          </div>
          <div v-if="application.type === 'adoption' && application.adoptionDetails" class="mb-6 space-y-1 text-lg">
            <h3 class="text-lg mb-2 underline">Результаты анкетирования</h3>
            <p v-for="(value, key) in application.adoptionDetails" :key="key">
                {{ adoptionFieldLabels[key] ?? key }}: {{ value }}
            </p>
          </div>
          
          <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
            {{ errorMessage }}
          </div>
          
          <p class="mb-2">Статус заявки</p>

          <div class="relative inline-block w-48 mb-6">
            <select
              v-model="localStatus"
              class="w-full appearance-none bg-transparent border-2 border-text-secondary rounded-xl px-4 py-2 pr-10"
              :disabled="isLoading">
              <option value="pending">Новая</option>
              <option value="in_progress">В работе</option>
              <option value="approved">Завершена</option> 
              <option value="rejected">Отклонено</option>
            </select>
            <span class="absolute right-4 top-1/2 -translate-y-1/2">^</span>
          </div>

          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              @click="saveStatus" 
              class="btn px-1 py-1"
              :disabled="isLoading">
              {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
            </button>
            <button 
              @click="handleContact" 
              class="secondary-btn px-1 py-1"
              :disabled="isLoading">
              Связаться
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>