<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <div class="mx-auto base-container p-9 py-3">
        <div class="max-w-4xl mx-auto card-bg rounded-2xl shadow-2xl border border-gray-200 p-8">
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl text-text-primary font-normal">{{ application.petName }}</h1>
            <span :class="['text-base font-normal px-6 py-1', getStatusClass(application.status)]">
              {{ getStatusText(application.status) }}
            </span>
          </div>

          <div class="space-y-2 mb-8">
            <p class="text-base text-text-secondary">{{ application.clientName }}</p>
            <p class="text-base text-text-secondary">{{ application.phone }}</p>
            <p v-if="application.email" class="text-base text-text-secondary">{{ application.email }}</p>
          </div>

          <div class="mb-8">
            <label class="text-base text-text-secondary block mb-2">Статус заявки</label>
            <select v-model="application.status" class="border rounded-lg px-3 py-2">
              <option value="pending">Новое</option>
              <option value="in_progress">В работе</option>
              <option value="approved">Принято</option>
              <option value="rejected">Отклонено</option>
            </select>
          </div>

          <div class="flex gap-4 mb-8">
            <button class="bg-accent text-white border-2 border-accent rounded-xl px-6 py-2 text-lg" @click="contactClient">Связаться</button>
            <button class="bg-accent text-white border-2 border-accent rounded-xl px-6 py-2 text-lg" @click="saveChanges">Сохранить</button>
          </div>

          <div class="flex justify-between items-center">
            <p class="text-sm text-text-secondary">{{ formatDate(application.createdAt) }}</p>
            <span class="font-normal px-3 py-2 rounded-lg text-text-secondary text-xl">
              {{ application.type === 'adoption' ? 'Забрать домой' : 'Опекунство' }}
            </span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref } from 'vue'

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
const applicationId = Number(route.params.id)

const applications = ref<Application[]>([
  { id: 1, petName: 'Марс', clientName: 'Иван Иванов', phone: '+8 (800) 555-35-35', type: 'adoption', status: 'pending', createdAt: new Date('2025-11-28T16:17:00') },
  { id: 2, petName: 'Лич', clientName: 'Иван Иванов', phone: '+8 (800) 555-35-35', type: 'adoption', status: 'in_progress', createdAt: new Date('2025-11-28T16:17:00') },
  { id: 3, petName: 'Лион', clientName: 'Иван Иванов', phone: '+8 (800) 555-35-35', type: 'custody', status: 'approved', createdAt: new Date('2025-11-28T16:17:00') },
  { id: 4, petName: 'Скайрас', clientName: 'Иван Иванов', phone: '+8 (800) 555-35-35', type: 'custody', status: 'rejected', createdAt: new Date('2025-11-28T16:17:00') },
  { id: 5, petName: 'Тоби', clientName: 'Мария Петрова', phone: '+8 (900) 123-45-67', email: 'maria@mail.ru', type: 'adoption', status: 'pending', createdAt: new Date('2025-11-29T10:30:00'), notes: 'Клиент интересуется особенностями ухода за собакой', petId: 1 },
  { id: 6, petName: 'Арчи', clientName: 'Алексей Смирнов', phone: '+8 (911) 222-33-44', email: 'alex@mail.ru', type: 'custody', status: 'in_progress', createdAt: new Date('2025-11-29T14:45:00'), notes: 'Хочет взять под опеку на 6 месяцев', petId: 2 }
])

const application = ref<Application>(applications.value.find(a => a.id === applicationId)!)

const getStatusText = (status: Application['status']) => ({
  pending: 'Новое',
  in_progress: 'В работе',
  approved: 'Принято',
  rejected: 'Отклонено'
}[status])

const getStatusClass = (status: Application['status']) => ({
  pending: 'bg-transparent text-blue-300 border-2 border-blue-300 rounded-full',
  in_progress: 'bg-transparent text-yellow-300 border-2 border-yellow-300 rounded-full',
  approved: 'bg-transparent text-green-300 border-2 border-green-300 rounded-full',
  rejected: 'bg-transparent text-red-300 border-2 border-red-300 rounded-full'
}[status])

const formatDate = (date: Date) => new Intl.DateTimeFormat('ru-RU', {
  day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit'
}).format(date).replace(',', '').replace(/\s+/g, '  ')

const contactClient = () => {
  window.location.href = `tel:${application.value.phone}`
}
const saveChanges = () => {
  console.log('Сохранено:', application.value)
}
</script>
