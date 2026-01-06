<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})

import { DogGender } from "~/types/dogGender"
import { apiFetch } from "~/composables/useAPI"
import { useTags } from '~/composables/useTags'

type Tag = Dog['tags'][number]

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()
const {  data: dog, pending, error } = await useAsyncData<Dog>(
  `dog-${route.params.id}`,
  () => apiFetch(`/dogs/${String(route.params.id)}`)
)

const {  data: availableTags, pending: tagsLoading } = useTags<Tag[]>() 
const isDeleteModalOpen = ref(false)
const deleteMessage = ref<string | null>(null)
const deleteStatus = ref<"none" | "success" | "error">("none")

function openDeleteModal() {
  isDeleteModalOpen.value = true
}

function closeDeleteModal() {
  isDeleteModalOpen.value = false
  deleteStatus.value = "none"
}

async function deleteDog() {
  if (!dog.value) return
  try {
    await apiFetch(`/dogs/${dog.value.id}`, { method: "DELETE" })
    deleteMessage.value = "Животное удалено успешно!"
    deleteStatus.value = "success"
    setTimeout(() => router.back(), 500)
  } catch {
    deleteMessage.value = "Ошибка удаления"
    deleteStatus.value = "error"
  }
}
const isInEditMode = ref(false)

const editName = ref("")
const editDescription = ref("")
const editAge = ref<number>(0)
const editGender = ref<DogGender>(DogGender.male)
const editVetPassport = ref(false)
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)
const editBreed = ref("Неизвестно") 
const selectedTagIds = ref<string[]>([])
const nameError = ref(false)
const descriptionError = ref(false)
const ageError = ref(false)
const isAddTagModalOpen = ref(false)
const newTagName = ref("")
const newTagError = ref(false)

async function createNewTag() {
  const name = newTagName.value.trim()
  if (!name) {
    newTagError.value = true
    return
  }

  try {
    const newTag: Tag = await apiFetch("/tags", {
      method: "POST",
      body: JSON.stringify({ name }),
      headers: { "Content-Type": "application/json" }
    })

    if (availableTags.value) {
      availableTags.value.push(newTag)
    }

    isAddTagModalOpen.value = false
    newTagName.value = ""
    newTagError.value = false
  } catch (e) {
    console.error("Ошибка создания тега:", e)
  }
}

function openAddTagModal() {
  isAddTagModalOpen.value = true
  newTagError.value = false
}

function closeAddTagModal() {
  isAddTagModalOpen.value = false
  newTagName.value = ""
  newTagError.value = false
}

const tagToDelete = ref<Tag | null>(null)
const isDeleteTagModalOpen = ref(false)
const deleteTagError = ref<string | null>(null)

function openDeleteTagModal(tag: Tag) {
  tagToDelete.value = tag
  isDeleteTagModalOpen.value = true
  deleteTagError.value = null
}

function closeDeleteTagModal() {
  isDeleteTagModalOpen.value = false
  tagToDelete.value = null
  deleteTagError.value = null
}

async function confirmDeleteTag() {
  if (!tagToDelete.value) return

  try {
    await apiFetch(`/tags/${tagToDelete.value.id}`, {
      method: "DELETE"
    })

    if (availableTags.value) {
      availableTags.value = availableTags.value.filter((t: Tag) => t.id !== tagToDelete.value!.id)
    }

    selectedTagIds.value = selectedTagIds.value.filter(id => id !== tagToDelete.value!.id.toString())

    closeDeleteTagModal()
  } catch (e: any) {
    deleteTagError.value = e.response?.data?.detail || "Невозможно удалить тег"
  }
}

const displayDeleteMessage = computed(() =>
  deleteStatus.value !== "none"
)

const deleteMessageClasses = computed(() => ({
  "text-success": deleteStatus.value === "success",
  "text-error": deleteStatus.value === "error"
}))

watch(dog, (newDog) => {
  if (newDog?.image_url) {
    previewImage.value = newDog.image_url
  } else {
    previewImage.value = null
  }
}, { immediate: true })

function backClicked() {
  router.back()
}

function toggleEditMode() {
  if (!dog.value) return

  if (!isInEditMode.value) {
    editName.value = dog.value.name
    editDescription.value = dog.value.description
    editAge.value = dog.value.age
    editGender.value = dog.value.gender
    editVetPassport.value = dog.value.veterinary_passport
    selectedTagIds.value = dog.value.tags.map(t => t.id.toString())
    selectedImage.value = null
  }
  isInEditMode.value = !isInEditMode.value
}

function triggerImageUpload() {
  document.getElementById("imageInput")?.click()
}

function handleImageChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  selectedImage.value = file
  const reader = new FileReader()
  reader.onload = e => (previewImage.value = e.target?.result as string)
  reader.readAsDataURL(file)
}

async function saveChanges() {
  if (!dog.value) return

  nameError.value = !editName.value.trim()
  descriptionError.value = !editDescription.value.trim()
  ageError.value = editAge.value <= 0

  if (nameError.value || descriptionError.value || ageError.value) return

  const formData = new FormData()
  formData.append("name", editName.value.trim())
  formData.append("age", editAge.value.toString())
  formData.append("breed", editBreed.value)
  formData.append("description", editDescription.value.trim())
  formData.append("gender", editGender.value)
  formData.append("veterinary_passport", String(editVetPassport.value))

  formData.append("tag_ids", selectedTagIds.value.join(","))

  if (selectedImage.value) {
    formData.append("file", selectedImage.value)
  }

  try {
    const updated = await apiFetch<Dog>(
      `/dogs/${dog.value.id}`,
      { method: "PATCH", body: formData }
    )
    dog.value = updated
    isInEditMode.value = false
  } catch (e) {
    console.error("Ошибка сохранения", e)
  }
}

function getImageUrl(path: string | null): string | undefined {
  if (!path) return undefined
  if (path.startsWith('data:')) return path
  return `${config.public.apiBase}${path}`
}
</script>

<template>
  <section class="flex flex-col gap-4 base-section">
    <div class="base-container mx-auto relative flex justify-center items-center mb-2">
      <svg class="absolute left-0 cursor-pointer" @click="backClicked" width="55" height="47"
        viewBox="0 0 55 47" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round" />
        <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
          stroke-linecap="round" />
      </svg>
      <h1 class="text-2xl text-primary font-bold">Животные</h1>
    </div>

    <div v-if="pending" class="text-center py-20 text-xl">Загрузка..</div>
    <div v-else-if="error" class="text-center py-20 text-error text-xl">Ошибка загрузки</div>
    <div v-else-if="dog" class="min-h-screen bg-bg font-cuprum">
      <main class="base-section pt-10">
        <div class="base-container mx-auto">
          <div class="card-bg rounded-2xl overflow-hidden shadow-lg">
            <div class="w-full h-96 bg-gray-200 relative">
              <img
                v-if="previewImage"
                :src="getImageUrl(previewImage)"
                :alt="dog.name"
                class="w-full h-full object-cover"/>
              <Icon v-else name="material-symbols:pets"
                class="absolute inset-0 m-auto text-6xl text-text-secondary" />
              <div v-if="isInEditMode"
                class="absolute inset-0 bg-black/30 flex items-center justify-center cursor-pointer"
                @click="triggerImageUpload">
                <button class="btn text-xl pointer-events-none">Изменить фотографию</button>
              </div>
              <input id="imageInput" type="file" accept="image/*" class="hidden" @change="handleImageChange" />
            </div>

            <div class="p-6">
              <h2 class="section-title text-center mb-4">
                {{ dog.name }}
              </h2>
              <div v-if="!isInEditMode" class="mb-6">
                <div v-if="dog.description" class="mb-4 text-text-primary text-lg">
                  <p>{{ dog.description }}</p>
                </div>
                <div class="mb-2 text-text-secondary text-lg">
                  <p>Пол: {{ dog.gender === DogGender.male ? 'Мужской' : 'Женский' }} </p>
                  <p>Возраст: {{ dog.age }} лет</p>
                  <p>Ветпаспорт: {{ dog.veterinary_passport ? 'есть' : 'нет' }}</p>
                </div>
                <div class="flex flex-wrap gap-2 mb-6 text-lg">
                  <span
                    v-for="tag in dog.tags"
                    :key="tag.id"
                    class="border-2 border-accent text-accent rounded-full px-4 py-1">
                    {{ tag.name }}
                  </span>
                </div>
              </div>

              <div v-else class="mb-6 text-text-secondary">
                <div class="mb-4">
                  <input
                    v-model="editName"
                    type="text"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
                    placeholder="Имя собаки"/>
                  <span v-if="nameError" class="text-error text-sm">Имя не может быть пустым</span>
                </div>

                <div class="mb-4">
                  <textarea
                    v-model="editDescription"
                    rows="3"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent resize-none"
                    placeholder="Описание">
                  </textarea>
                  <span v-if="descriptionError" class="text-error text-sm">Описание не может быть пустым</span>
                </div>

                <div class="flex flex-col gap-4 mb-4 text-text-secondary">
                  <div>
                    <label class="block mb-2">Возраст (лет)</label>
                    <input
                      v-model.number="editAge"
                      type="number"
                      min="0"
                      class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"/>
                    <span v-if="ageError" class="text-error text-sm">Возраст должен быть больше 0</span>
                  </div>

                  <div>
                    <label class="block mb-2">Пол</label>
                    <div class="flex gap-4">
                      <label class="flex items-center gap-2 cursor-pointer font-normal">
                        <input
                          type="radio"
                          :value="DogGender.male"
                          v-model="editGender"
                          class="w-4 h-4 accent-accent"/>
                        <span>Мужской</span>
                      </label>
                      <label class="flex items-center gap-2 cursor-pointer font-normal">
                        <input
                          type="radio"
                          :value="DogGender.female"
                          v-model="editGender"
                          class="w-4 h-4 accent-accent"/>
                        <span>Женский</span>
                      </label>
                    </div>
                  </div>
                </div>

                <div class="mb-4 text-text-secondary">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <span>Ветеринарный паспорт</span>
                    <input
                      type="checkbox"
                      v-model="editVetPassport"
                      class="peer sr-only"/>
                    <span class="relative flex items-center justify-center w-5 h-5 rounded-md border-2 border-input-border peer-checked:border-accent peer-checked:bg-accent transition-all duration-200">
                      <svg
                        v-if="editVetPassport"
                        class="w-3 h-3 text-white pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="3">
                        <path d="M5 13l4 4L19 7"/>
                      </svg>
                    </span>
                  </label>
                </div>
                <div class="mb-6">
                  <div v-if="tagsLoading" class="text-sm text-text-secondary">Загрузка тегов..</div>
                  <div v-else class="flex flex-wrap items-center gap-2">
                    <template v-if="availableTags?.length">
                      <div
                        v-for="tag in availableTags"
                        :key="tag.id"
                        class="group relative flex items-center gap-2">
                        <label class="cursor-pointer flex items-center gap-2">
                          <input
                            type="checkbox"
                            :value="tag.id.toString()"
                            v-model="selectedTagIds"
                            class="sr-only peer"/>
                          <span
                            class="relative overflow-hidden border rounded-full px-5 py-3 pr-9 text-base font-medium transition-colors duration-150"
                            :class="selectedTagIds.includes(tag.id.toString())
                              ? 'text-accent border-accent border-2'
                              : 'text-text-secondary border-gray-300 border-2'">
                            {{ tag.name }}
                          </span>
                        </label>
                        <button
                          type="button"
                          @click.stop="openDeleteTagModal(tag)"
                          class="absolute top-1/2 right-2 -translate-y-1/2 w-5 h-5 rounded-full bg-transparent text-accent flex items-center justify-center opacity-0 translate-x-4 group-hover:opacity-100 group-hover:translate-x-0 hover:bg-red-500 hover:text-white transition-all duration-200 ease-out"
                          title="Удалить тег">
                          <svg
                            viewBox="0 0 24 24"
                            class="w-3.5 h-3.5"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.75"
                            stroke-linecap="round"
                            stroke-linejoin="round">
                            <path d="M6 6l12 12" />
                            <path d="M18 6l-12 12" />
                          </svg>
                        </button>
                      </div>
                    </template>
                    <button
                      type="button"
                      @click="openAddTagModal"
                      class="ml-2 w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center text-lg hover:bg-opacity-90 transition-opacity"
                      title="Добавить новый тег">
                      +
                    </button>
                  </div>
                  <div
                    v-if="!tagsLoading && (!availableTags || availableTags.length === 0)"
                    class="text-sm text-text-secondary">
                    Нет доступных тегов
                  </div>
                </div>
              </div>
              <div class="flex flex-col gap-2 sm:flex-row sm:gap-2 w-full">
                <button v-if="!isInEditMode" class="btn flex-1" @click="toggleEditMode">Редактировать</button>
                <button v-else class="btn flex-1" @click="saveChanges">Сохранить</button>
                <button class="secondary-btn flex-1" @click="openDeleteModal">Удалить</button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
    <Modal title="Удаление карточки" :is-open="isDeleteModalOpen" @close="closeDeleteModal">
      <div class="flex flex-col gap-4 p-4">
        <span>Удалить карточку «{{ dog?.name }}»?</span>
        <span v-if="displayDeleteMessage" :class="deleteMessageClasses">
          {{ deleteMessage }}
        </span>
        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeDeleteModal">Отмена</button>
          <button class="btn" @click="deleteDog">Удалить</button>
        </div>
      </div>
    </Modal>
    <Modal
      v-if="isAddTagModalOpen"
      title="Создать тег"
      :is-open="isAddTagModalOpen"
      @close="closeAddTagModal">
      <div class="flex flex-col gap-4 p-4">
        <div>
          <label class="block text-text-secondary mb-2">Название тега</label>
          <input
            v-model="newTagName"
            type="text"
            class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
            placeholder="Например: Дружелюбный"
            @keyup.enter="createNewTag"/>
          <span v-if="newTagError" class="text-error text-sm mt-1">Поле не может быть пустым</span>
        </div>
        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeAddTagModal">Отмена</button>
          <button class="btn" @click="createNewTag">Создать</button>
        </div>
      </div>
    </Modal>
    <Modal
      v-if="isDeleteTagModalOpen"
      title="Удалить тег"
      :is-open="isDeleteTagModalOpen"
      @close="closeDeleteTagModal">
      <div class="flex flex-col gap-4 p-4">
        <p>Удалить тег «{{ tagToDelete?.name }} »?</p>
        <p class="text-sm text-text-secondary">Это действие нельзя отменить. Убедитесь, что тег не используется.</p>
        <span v-if="deleteTagError" class="text-accent text-sm">{{ deleteTagError }}</span>
        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeDeleteTagModal">Отмена</button>
          <button class="btn" @click="confirmDeleteTag">Удалить</button>
        </div>
      </div>
    </Modal>
  </section>
</template>