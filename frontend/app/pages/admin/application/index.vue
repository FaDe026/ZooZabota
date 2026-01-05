<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <div class="mx-auto base-container p-9 py-3">
        <div v-if="pending" class="text-center py-20">
          Загрузка..
        </div>
        <div v-else class="max-w-6xl mx-auto">
          <div class="mb-10 text-center">
            <h1 class="text-2xl text-text-primary mb-8 font-normal">
              Заявки
            </h1>
            <div class="flex flex-wrap gap-2 mb-10 justify-center">
              <button
                v-for="filter in filters"
                :key="filter.id"
                @click="activeFilter = filter.id"
                :class="[
                  'rounded-xl font-normal text-lg whitespace-nowrap px-9 py-1',
                  activeFilter === filter.id
                    ? 'base-card text-accent border-2 border-accent'
                    : 'base-card'
                ]">
                {{ filter.name }}
              </button>
            </div>
          </div>
          <div v-if="filteredApplications.length === 0" class="text-center py-10">
            <p class="text-lg">Заявки не найдены</p>
          </div>
          <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div
              v-for="application in filteredApplications"
              :key="application.id"
              class="card-bg rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
              <div class="p-4">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="text-xl">
                    {{ application.petName }}
                  </h2>
                  <span :class="getStatusClass(application.status)">
                    {{ getStatusText(application.status) }}
                  </span>
                </div>
                <div class="flex justify-between items-start mb-4">
                  <div class="text-text-secondary">
                    <p>{{ application.clientName }}</p>
                    <p>{{ application.phone }}</p>
                  </div>
                  <NuxtLink
                    :to="`/admin/application/${application.id}`"
                    class="bg-accent text-white rounded-xl px-4 py-2">
                    Просмотр
                  </NuxtLink>
                </div>
                <div class="flex justify-between items-center">
                  <p class="text-sm text-text-secondary">
                    {{ formatDate(application.createdAt) }}
                  </p>
                  <span class="text-text-secondary text-xl">
                    {{ application.type === 'adoption'
                      ? 'Забрать домой'
                      : 'Опекунство' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

interface RequestApiResponse {
  id: number
  dog_id: number
  full_name: string
  phone: string
  email: string | null
  status: string
  type: string
  created_at: string
}

interface DogApiResponse {
  id: number
  name: string
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
}

type FilterType = 'all' | 'adoption' | 'custody'

const filters = [
  { id: 'all', name: 'Все' },
  { id: 'adoption', name: 'Забрать домой' },
  { id: 'custody', name: 'Опекунство' }
] as const

const activeFilter = ref<FilterType>('all')

const fetchDogName = async (dogId: number): Promise<string> => {
  try {
    const dog = await $fetch<DogApiResponse>(
      `http://localhost:8000/dogs/${dogId}`
    )
    return dog.name
  } catch {
    return `Собака #${dogId}`
  }
}

const { data, pending } = await useAsyncData(
  'requests',
  async () => {
    const response = await $fetch<RequestApiResponse[]>(
      'http://localhost:8000/requests'
    )

    const dogNameMap = new Map<number, string>()
    const dogIds = [...new Set(response.map(r => r.dog_id).filter(Boolean))]

    await Promise.all(
      dogIds.map(async id => {
        dogNameMap.set(id, await fetchDogName(id))
      })
    )

    return response.map(r => ({
      id: r.id,
      petName: r.dog_id
        ? dogNameMap.get(r.dog_id) ?? `Собака #${r.dog_id}`
        : 'Питомец не указан',
      clientName: r.full_name,
      phone: r.phone,
      email: r.email ?? undefined,
      type: r.type === 'Усыновление' ? 'adoption' : 'custody',
      status: ({
        'Новая': 'pending',
        'В работе': 'in_progress',
        'Принято': 'approved',
        'Отклонено': 'rejected'
      } as any)[r.status] ?? 'pending',
      createdAt: new Date(r.created_at),
      petId: r.dog_id
    }))
  },
  { default: () => [] }
)

const applications = computed(() => data.value)

const filteredApplications = computed(() => {
  if (activeFilter.value === 'adoption') {
    return applications.value.filter(a => a.type === 'adoption')
  }
  if (activeFilter.value === 'custody') {
    return applications.value.filter(a => a.type === 'custody')
  }
  return applications.value
})

const getStatusText = (s: Application['status']) => ({
  pending: 'Новая',
  in_progress: 'В работе',
  approved: 'Принято',
  rejected: 'Отклонено'
}[s])

const getStatusClass = (s: Application['status']) => ({
  pending: 'border-blue-300 text-blue-300 border-2 px-4 rounded-full',
  in_progress: 'border-yellow-300 text-yellow-300 border-2 px-4 rounded-full',
  approved: 'border-green-300 text-green-300 border-2 px-4 rounded-full',
  rejected: 'border-red-300 text-red-300 border-2 px-4 rounded-full'
}[s])

const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
</script>
