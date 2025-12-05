<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <div class="mx-auto base-container p-9 py-3">
        <div class="max-w-6xl mx-auto">
          <div class="mb-10 text-center">
            <h1 class="text-2xl text-text-primary mb-8 font-normal">Заявки</h1>
            <div class="flex flex-wrap gap-2 mb-10 justify-center">
                <button 
                  v-for="filter in filters" 
                  :key="filter.id"
                  @click="activeFilter = filter.id"
                  :class="[
                    'rounded-xl font-normal text-lg whitespace-nowrap px-11 py-1', 
                    activeFilter === filter.id 
                      ? 'base-card text-accent border-2 border-accent' 
                      : 'base-card'
                  ]">
                  {{ filter.name }}
                </button>
            </div>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div 
              v-for="application in filteredApplications" 
              :key="application.id" 
              class="card-bg rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
              <div class="p-4">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="text-xl text-text-primary font-normal">{{ application.petName }}</h2>
                  <span 
                    :class="[
                      'text-base font-normal px-6 py-1',
                      getStatusClass(application.status)
                    ]"
                  >
                    {{ getStatusText(application.status) }}
                  </span>
                </div>
                <div class="flex justify-between items-start mb-4">
                  <div class="space-y-1">
                    <p class="text-base text-text-secondary">{{ application.clientName }}</p>
                    <p class="text-base text-text-secondary">{{ application.phone }}</p>
                  </div>
                    <button 
                        @click="toggleApplicationDetails(application.id)"
                        class="bg-accent text-white border-2 border-accent rounded-xl px-4 py-2 text-xl">
                        Просмотр
                    </button>
                </div>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-text-secondary">{{ formatDate(application.createdAt) }}</p>
                    <span class="font-normal px-3 py-2 rounded-lg text-text-secondary text-xl">
                    {{ application.type === 'adoption' ? 'Забрать домой' : 'Опекунство' }}
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
interface Application {
  id: number
  petName: string
  clientName: string
  phone: string
  email?: string
  type: 'adoption' | 'custody'
  status: 'pending' | 'in_progress' | 'approved' | 'rejected'
  createdAt: Date
  notes?: string
  petId?: number
}

definePageMeta({
  layout: 'default'
})
const filters = [
  { id: 1, name: 'Все' },
  { id: 2, name: 'Забрать домой' },
  { id: 3, name: 'Опекунство' }
]

const activeFilter = ref(1)
const expandedApplications = ref<number[]>([]) 

const applications = ref<Application[]>([
  {
    id: 1,
    petName: 'Марс',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    type: 'adoption',
    status: 'pending',
    createdAt: new Date('2025-11-28T16:17:00')
  },
  {
    id: 2,
    petName: 'Лич',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    type: 'adoption',
    status: 'in_progress',
    createdAt: new Date('2025-11-28T16:17:00')
  },
  {
    id: 3,
    petName: 'Лион',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    type: 'custody',
    status: 'approved',
    createdAt: new Date('2025-11-28T16:17:00')
  },
  {
    id: 4,
    petName: 'Скайрас',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    type: 'custody',
    status: 'rejected',
    createdAt: new Date('2025-11-28T16:17:00')
  },
  {
    id: 5,
    petName: 'Тоби',
    clientName: 'Мария Петрова',
    phone: '+8 (900) 123-45-67',
    email: 'maria@mail.ru',
    type: 'adoption',
    status: 'pending',
    createdAt: new Date('2025-11-29T10:30:00'),
    notes: 'Клиент интересуется особенностями ухода за собакой',
    petId: 1
  },
  {
    id: 6,
    petName: 'Арчи',
    clientName: 'Алексей Смирнов',
    phone: '+8 (911) 222-33-44',
    email: 'alex@mail.ru',
    type: 'custody',
    status: 'in_progress',
    createdAt: new Date('2025-11-29T14:45:00'),
    notes: 'Хочет взять под опеку на 6 месяцев',
    petId: 2
  }
])

const filteredApplications = computed(() => {
  if (activeFilter.value === 1) return applications.value
  if (activeFilter.value === 2) return applications.value.filter(app => app.type === 'adoption')
  if (activeFilter.value === 3) return applications.value.filter(app => app.type === 'custody')
  return applications.value
})

const getApplicationsByStatus = (status: Application['status']) => {
  return applications.value.filter(app => app.status === status)
}

const getStatusText = (status: Application['status']) => {
  return {
    'pending': 'Новое',
    'in_progress': 'В работе',
    'approved': 'Принято',
    'rejected': 'Отклонено'
  }[status]
}

const getStatusClass = (status: Application['status']) => {
  return {
    'pending': 'bg-transparent text-blue-300 border-2 border-blue-300 rounded-full',
    'in_progress': 'bg-transparent text-yellow-300 border-2 border-yellow-300 rounded-full',
    'approved': 'bg-transparent text-green-300 border-2 border-green-300 rounded-full',
    'rejected': 'bg-transparent text-red-300 border-2 border-red-300 rounded-full'
  }[status]
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date).replace(',', '').replace(/\s+/g, '  ')
}

const toggleApplicationDetails = (applicationId: number) => {
  const index = expandedApplications.value.indexOf(applicationId)
  if (index > -1) {
    expandedApplications.value.splice(index, 1)
  } else {
    expandedApplications.value.push(applicationId)
  }
}

const changeApplicationStatus = (applicationId: number, newStatus: Application['status']) => {
  const application = applications.value.find(app => app.id === applicationId)
  if (application) {
    application.status = newStatus
  }
}
const fetchApplications = async () => {
  try {
    console.log('Загрузка заявок...')
    
  } catch (error) {
    console.error('Ошибка при загрузке заявок:', error)
  }
}

onMounted(() => {
  fetchApplications()
})
</script>