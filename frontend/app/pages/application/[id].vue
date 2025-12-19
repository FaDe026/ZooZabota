<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <h1 class="text-3xl text-text-primary mb-8 text-center">
        {{ pageTitle }}
      </h1>

      <div class="mx-auto base-container p-9 py-3 max-w-3xl">
        <div class="base-card rounded-2xl p-8 shadow-xl relative">
          <span
            :class="[
              'absolute top-6 right-6 text-base font-normal px-6 py-1',
              getStatusClass(application.status)]">
            {{ getStatusText(application.status) }}
          </span>
          <h1 class="text-2xl text-text-primary mb-8 text-center">
            {{ application.petName }}
          </h1>
          <div class="space-y-1 text-base text-text-secondary">
            <p>{{ application.clientName }}</p>
            <p>{{ application.phone }}</p>
            <p v-if="application.email">{{ application.email }}</p>
            <div class="pt-3">
              <p class="text-base text-text-secondary">
                Статус заявки
              </p>

              <div class="relative inline-block">
              <select
                v-model="application.status"
                class="appearance-none bg-transparent border-2 border-text-secondary rounded-xl
                      px-4 py-1 pr-10
                      text-base text-text-secondary
                      focus:outline-none focus:ring-0">
                <option value="pending">Новое</option>
                <option value="in_progress">В работе</option>
                <option value="approved">Принято</option>
                <option value="rejected">Отклонено</option>
              </select>
              <span
                class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary">
                ^
              </span>
            </div>

            </div>
          </div>
          <div class="mt-8 flex justify-center gap-4">
            <button
              type="button"
              @click="handleContact"
              class="border-2 border-accent text-accent rounded-xl px-6 py-1 text-base leading-tight hover:bg-accent hover:text-white transition">
              Связаться
            </button>

            <button
              type="button"
              @click="handleSave"
              class="bg-accent text-white rounded-xl px-6 py-1 text-base leading-tight hover:opacity-90 transition">
              Сохранить
            </button>
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

const route = useRoute()
const applicationId = Number(route.params.id)

const applications: Application[] = [
  {
    id: 1,
    petName: 'Марс',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    email: '123@mail.ru',
    type: 'adoption',
    status: 'pending',
    createdAt: new Date('2025-11-28T16:17:00')
  },
  {
    id: 2,
    petName: 'Лич',
    clientName: 'Иван Иванов',
    phone: '+8 (800) 555-35-35',
    email: '123@mail.ru',
    type: 'custody',
    status: 'in_progress',
    createdAt: new Date('2025-11-28T16:17:00')
  }
]

const application = applications.find(app => app.id === applicationId)

if (!application) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Заявка не найдена'
  })
}

const getStatusText = (status: Application['status']) => {
  return {
    pending: 'Новое',
    in_progress: 'В работе',
    approved: 'Принято',
    rejected: 'Отклонено'
  }[status]
}

const getStatusClass = (status: Application['status']) => {
  return {
    pending: 'bg-transparent text-blue-300 border-2 border-blue-300 rounded-full',
    in_progress: 'bg-transparent text-yellow-300 border-2 border-yellow-300 rounded-full',
    approved: 'bg-transparent text-green-300 border-2 border-green-300 rounded-full',
    rejected: 'bg-transparent text-red-300 border-2 border-red-300 rounded-full'
  }[status]
}

const pageTitle = computed(() => {
  return application.type === 'adoption'
    ? 'Заявка забрать домой'
    : 'Заявка на опекунство'
})

const handleContact = () => {
  if (application.email) {
    window.location.href = `mailto:${application.email}`
  } else {
    window.location.href = `tel:${application.phone.replace(/\s|\(|\)|-/g, '')}`
  }
}

const handleSave = () => {
  console.log('Сохранено:', application)
  alert('Изменения сохранены')
}
</script>
