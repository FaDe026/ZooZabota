<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="pt-10 px-4 sm:px-8 md:px-16 lg:px-24">
      <div class="mx-auto max-w-[1200px] p-9 py-3">
        <div v-if="application" class="max-w-xl mx-auto">
          <h1 class="text-2xl text-text-primary mb-6 font-normal text-center">
            {{ application.type === 'custody' ? 'Заявка на опекунство' : 'Заявка на усыновление' }}
          </h1>

          <div class="bg-white/90 rounded-2xl shadow-2xl border border-gray-200 px-6 py-6 relative">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl text-text-primary font-normal text-center w-full">
                {{ application.petName }}
              </h2>

              <span
                class="text-base font-normal px-6 py-1 rounded-full border-2"
                :class="{
                  'text-blue-500 border-blue-500': application.status === 'pending',
                  'text-yellow-500 border-yellow-500': application.status === 'in_progress',
                  'text-green-500 border-green-500': application.status === 'approved',
                  'text-red-500 border-red-500': application.status === 'rejected'
                }"
              >
                {{ getStatusText(application.status) }}
              </span>
            </div>

            <div class="space-y-3 mb-6">
              <div>
                <p class="text-sm text-text-secondary mb-1">Клиент:</p>
                <p class="text-base text-text-primary">{{ application.clientName }}</p>
              </div>
              
              <div>
                <p class="text-sm text-text-secondary mb-1">Телефон:</p>
                <p class="text-base text-text-primary">{{ application.phone }}</p>
              </div>
              
              <div v-if="application.email">
                <p class="text-sm text-text-secondary mb-1">Email:</p>
                <p class="text-base text-text-primary">{{ application.email }}</p>
              </div>
              
              <div>
                <p class="text-sm text-text-secondary mb-1">Дата создания:</p>
                <p class="text-base text-text-primary">{{ formatDate(application.createdAt) }}</p>
              </div>
              
              <div>
                <p class="text-sm text-text-secondary mb-1">Тип заявки:</p>
                <p class="text-base text-text-primary">
                  {{ application.type === 'custody' ? 'Опекунство' : 'Усыновление' }}
                </p>
              </div>
              
              <div v-if="application.notes">
                <p class="text-sm text-text-secondary mb-1">Примечания:</p>
                <p class="text-base text-text-primary whitespace-pre-line">{{ application.notes }}</p>
              </div>
            </div>

            <div class="mb-6">
              <p class="text-base text-text-secondary mb-2">Статус заявки:</p>
              <select
                v-model="localStatus"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 text-text-primary bg-white text-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
              >
                <option value="pending">Новое</option>
                <option value="in_progress">В работе</option>
                <option value="approved">Принято</option>
                <option value="rejected">Отклонено</option>
              </select>
            </div>

            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                @click="goBack"
                class="px-8 py-2 rounded-xl border-2 border-accent text-accent text-xl bg-transparent hover:bg-accent hover:text-white transition-colors duration-300 ease-in-out"
              >
                Назад
              </button>
              
              <button
                @click="saveStatus"
                class="px-8 py-2 rounded-xl bg-accent text-white text-xl border-2 border-accent hover:bg-accent/90 transition-colors duration-300 ease-in-out"
              >
                Сохранить
              </button>
            </div>
          </div>
        </div>

        <div
          v-else
          class="text-center mt-10"
        >
          <p class="text-xl text-red-500 mb-4">Заявка не найдена</p>
          <div class="mt-4">
            <button
              @click="goBack"
              class="px-8 py-2 rounded-xl border-2 border-accent text-accent text-xl bg-transparent hover:bg-accent hover:text-white transition-colors duration-300 ease-in-out"
            >
              Вернуться к списку
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

definePageMeta({
  layout: 'default'
})

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

const route = useRoute()
const router = useRouter()

// Получаем ID из параметров маршрута
const id = computed(() => {
  const routeId = route.params.id
  const numId = Number(routeId)
  console.log('Route ID:', routeId, 'Parsed ID:', numId)
  return numId
})

// Для отладки
console.log('Application detail page loaded')
console.log('Route params:', route.params)
console.log('Application ID from URL:', id.value)

// Данные заявок
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

// Находим текущую заявку
const application = computed(() => {
  console.log('Searching for application with ID:', id.value)
  const found = applications.value.find(app => app.id === id.value)
  console.log('Found application:', found)
  return found
})

// Локальное состояние для редактирования
const localStatus = ref(application.value?.status || 'pending')

// Следим за изменением application и обновляем localStatus
watch(application, (newApp) => {
  if (newApp) {
    localStatus.value = newApp.status
  }
}, { immediate: true })

// Функция сохранения статуса
const saveStatus = () => {
  if (application.value) {
    console.log('Saving status:', localStatus.value, 'for application:', application.value.id)
    application.value.status = localStatus.value as Application['status']
    
    // Показываем уведомление об успешном сохранении
    alert('Статус заявки успешно обновлен!')
    
    // Можно добавить возврат к списку
    // goBack()
  }
}

// Функция возврата к списку
const goBack = () => {
  router.push('/applications')
}

// Функция для получения текста статуса
const getStatusText = (status: Application['status']) => {
  const statusMap = {
    pending: 'Новое',
    in_progress: 'В работе',
    approved: 'Принято',
    rejected: 'Отклонено'
  }
  return statusMap[status] || status
}

// Функция для форматирования даты
const formatDate = (date: Date) => {
  try {
    return new Intl.DateTimeFormat('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(date))
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Дата не указана'
  }
}
</script>