<template>
  <div class="min-h-screen bg-bg font-cuprum">
    <main class="base-section pt-10">
      <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl text-center mb-8">
            {{ pageTitle }}
          </h1>
          
          <NuxtLink 
            to="/admin/application" 
            class="text-accent hover:underline">
            Назад к списку
          </NuxtLink>
        </div>

        <div v-if="pending" class="text-center py-20">
          Загрузка...
        </div>

        <div v-else-if="application" class="max-w-xl mx-auto base-card p-8">
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Информация о клиенте</h2>
            <div class="space-y-2">
              <p><span class="font-medium">Имя:</span> {{ application.clientName }}</p>
              <p><span class="font-medium">Телефон:</span> {{ application.phone }}</p>
              <p v-if="application.email"><span class="font-medium">Email:</span> {{ application.email }}</p>
            </div>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Информация о питомце</h2>
            <p>{{ application.petName }}</p>
          </div>

          <div v-if="application.type === 'adoption' && application.adoptionDetails" class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Детали усыновления</h2>
            <div class="space-y-2">
              <p><span class="font-medium">Количество членов семьи:</span> {{ application.adoptionDetails.familyMemberCount }}</p>
              <p><span class="font-medium">Опыт содержания питомцев:</span> {{ application.adoptionDetails.hadExperienceAdoptionPet }}</p>
              <p><span class="font-medium">Цель усыновления:</span> {{ application.adoptionDetails.adoptionPurpose }}</p>
              <p><span class="font-medium">Тип жилья:</span> {{ application.adoptionDetails.housingType }}</p>
              <p><span class="font-medium">Площадь жилья:</span> {{ application.adoptionDetails.housingArea }}</p>
            </div>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Дата заявки</h2>
            <p>{{ formatDate(application.createdAt) }}</p>
          </div>

          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4">Статус заявки</h2>
            <select 
              v-model="application.status" 
              class="w-full p-2 border border-gray-300 rounded-lg">
              <option value="pending">Новая</option>
              <option value="in_progress">В работе</option>
              <option value="approved">Принято</option>
              <option value="rejected">Отклонено</option>
            </select>
          </div>

          <div class="flex gap-4">
            <button 
              @click="handleSave" 
              class="bg-accent text-white rounded-xl px-6 py-3 hover:bg-accent-dark transition">
              Сохранить изменения
            </button>
            
            <button 
              @click="goBack" 
              class="bg-gray-300 text-gray-700 rounded-xl px-6 py-3 hover:bg-gray-400 transition">
              Отмена
            </button>
          </div>
        </div>

        <div v-else class="text-center py-20">
          <p>Заявка не найдена</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })

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
  closed_at: string | null
  adoption_request: {
    family_member_count: string
    had_experience_adoption_pet: string
    adoption_purpose: string
    housing_type: string
    housing_area: string
  } | null
  guardian_request: {} | null
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
  adoptionDetails?: {
    familyMemberCount: string
    hadExperienceAdoptionPet: string
    adoptionPurpose: string
    housingType: string
    housingArea: string
  }
}

const application = ref<Application | null>(null)

const { pending } = await useAsyncData(
  `request-${applicationId}`,
  async () => {
    try {
      const response = await $fetch<RequestApiResponse>(
        `http://localhost:8000/requests/${applicationId}`
      )
      const getStatusKey = (status: string): Application['status'] => {
        const statusMap: Record<string, Application['status']> = {
          'Новая': 'pending',
          'В работе': 'in_progress',
          'Принято': 'approved',
          'Отклонено': 'rejected'
        }
        return statusMap[status] || 'pending'
      }
      const getType = (type: string): 'adoption' | 'custody' => {
        return type === 'Усыновление' ? 'adoption' : 'custody'
      }
      const petName = response.dog_id === 0 
        ? 'Питомец не указан' 
        : `Собака #${response.dog_id}`
      
      application.value = {
        id: response.id,
        petName: petName,
        clientName: response.full_name,
        phone: response.phone,
        email: response.email ?? undefined,
        type: getType(response.type),
        status: getStatusKey(response.status),
        createdAt: new Date(response.created_at),
        petId: response.dog_id
      }
      if (response.adoption_request) {
        application.value.adoptionDetails = {
          familyMemberCount: response.adoption_request.family_member_count,
          hadExperienceAdoptionPet: response.adoption_request.had_experience_adoption_pet,
          adoptionPurpose: response.adoption_request.adoption_purpose,
          housingType: response.adoption_request.housing_type,
          housingArea: response.adoption_request.housing_area
        }
      }
      
      return response
    } catch (error) {
      console.error('Ошибка при загрузке заявки:', error)
      return null
    }
  },
  {
    server: true,
    lazy: false
  }
)

const handleSave = async () => {
  if (!application.value) return

  try {
    const getStatusText = (status: Application['status']): string => {
      const statusMap: Record<Application['status'], string> = {
        'pending': 'Новая',
        'in_progress': 'В работе',
        'approved': 'Принято',
        'rejected': 'Отклонено'
      }
      return statusMap[status]
    }
    
    await $fetch(
      `http://localhost:8000/requests/${applicationId}`,
      {
        method: 'PATCH',
        body: { 
          status: getStatusText(application.value.status)
        }
      }
    )

    alert('Изменения сохранены')
    router.push('/admin/application')
  } catch (error) {
    console.error('Ошибка при сохранении:', error)
    alert('Ошибка при сохранении')
  }
}

const goBack = () => {
  router.push('/admin/application')
}

const pageTitle = computed(() => {
  if (!application.value) return 'Заявка'
  
  return application.value.type === 'adoption'
    ? 'Заявка на усыновление'
    : 'Заявка на опеку'
})

const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
</script>