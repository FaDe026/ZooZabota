<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})

import { DogGender } from '~/types/dogGender'
import { apiFetch } from "~/composables/useAPI"
import { useTags } from '~/composables/useTags'

// Тип тега: извлекаем из глобального Dog
type Tag = Dog['tags'][number]

const router = useRouter()

const editName = ref("")
const editDescription = ref("")
const editAge = ref<number>(0)
const editGender = ref<DogGender>(DogGender.male)
const editVetPassport = ref(false)
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)

// ОБЯЗАТЕЛЬНО для бэкенда
const editBreed = ref("Неизвестно")

const nameError = ref(false)
const descriptionError = ref(false)
const ageError = ref(false)

// Выбранные ID тегов
const selectedTagIds = ref<number[]>([])

// Загрузка существующих тегов
const {  data: availableTags, pending: tagsLoading } = useTags<Tag[]>()

// === Модалка создания тега ===
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

// === Модалка удаления тега ===
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

    selectedTagIds.value = selectedTagIds.value.filter(id => id !== tagToDelete.value!.id)

    closeDeleteTagModal()
  } catch (e: any) {
    deleteTagError.value = e.response?.data?.detail || "Невозможно удалить тег"
  }
}

// === Основная логика ===
function backClicked() {
  router.back()
}

function handleImageChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  selectedImage.value = file
  const reader = new FileReader()
  reader.onload = e => previewImage.value = e.target?.result as string
  reader.readAsDataURL(file)
}

function triggerImageUpload() {
  document.getElementById("imageInput")?.click()
}

async function saveChanges() {
  nameError.value = !editName.value.trim()
  descriptionError.value = !editDescription.value.trim()
  ageError.value = editAge.value <= 0

  if (nameError.value || descriptionError.value || ageError.value) {
    return
  }

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
    await apiFetch("/dogs", {
      method: "POST",
      body: formData
    })
    router.back()
  } catch (e) {
    console.error("Ошибка добавления собаки:", e)
  }
}

function cancelAdd() {
  router.back()
}
</script>

<template>
  <section class="flex flex-col gap-4 base-section">
    <div class="base-container mx-auto relative flex justify-center items-center mb-2">
      <svg class="absolute left-0 cursor-pointer" @click="backClicked()" width="55" height="47"
        viewBox="0 0 55 47" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round"
          stroke-linejoin="round" />
        <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
          stroke-linecap="round" stroke-linejoin="round" />
      </svg>

      <h1 class="text-2xl text-primary text-center font-bold">Добавить питомца</h1>
    </div>
    <div class="min-h-screen bg-bg font-cuprum">
      <main class="base-section pt-10">
        <div class="flex flex-col gap-2 mx-auto base-container">
          <div class="flex justify-center">
            <div class="card-bg rounded-2xl overflow-hidden shadow-lg border border-gray-200 w-full">
              <div
                class="w-full h-96 bg-gray-200 flex items-center justify-center overflow-hidden relative">
                <img v-if="previewImage" :src="previewImage" alt="Предпросмотр"
                  class="w-full h-full object-cover">
                <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />

                <div class="absolute inset-0 bg-black/20 bg-opacity-50 flex items-center justify-center cursor-pointer"
                  @click="triggerImageUpload">
                  <button type="button" class="btn text-xl pointer-events-none">
                    {{ previewImage ? 'Изменить фотографию' : 'Добавить фотографию' }}
                  </button>
                </div>
                <input type="file" id="imageInput" accept="image/*" class="hidden"
                  @change="handleImageChange">
              </div>

              <div class="p-6">
                <div class="mb-4">
                  <TextInput v-model="editName" placeholder="Имя собаки" />
                  <span v-if="nameError" class="text-error text-sm">Имя не может быть пустым</span>
                </div>

                <div class="mb-6">
                  <div
                    class="border-2 border-input-border px-4 py-3 rounded-xl focus-within:border-accent transition-colors">
                    <textarea v-model="editDescription" placeholder="Описание" rows="4"
                      class="focus:outline-0 w-full text-text-secondary resize-none"></textarea>
                  </div>
                  <span v-if="descriptionError" class="text-error text-sm">Описание не может быть
                    пустым</span>
                </div>

                <div class="flex flex-col gap-4 mb-6">
                  <div>
                    <span class="text-text-secondary block mb-2">Пол:</span>
                    <div class="flex gap-4">
                      <LabeledRadio name="gender" :value="DogGender.male" v-model="editGender">
                        Мужской
                      </LabeledRadio>
                      <LabeledRadio name="gender" :value="DogGender.female" v-model="editGender">
                        Женский
                      </LabeledRadio>
                    </div>
                  </div>

                  <div>
                    <span class="text-text-secondary block mb-2">Возраст (лет):</span>
                    <div
                      class="border-2 border-input-border px-4 py-3 rounded-xl focus-within:border-accent transition-colors">
                      <input type="number" v-model.number="editAge" min="0" placeholder="Возраст"
                        class="focus:outline-0 w-full text-text-secondary">
                    </div>
                    <span v-if="ageError" class="text-error text-sm">Возраст должен быть больше
                      0</span>
                  </div>

                  <div>
                    <LabeledCheckbox postion="after" name="vetPassport" v-model="editVetPassport">
                      Ветпаспорт:
                    </LabeledCheckbox>
                  </div>
                </div>

                <!-- БЛОК ТЕГОВ С КНОПКОЙ "+" И КРЕСТИКОМ -->
                <div class="mb-6">
                  <span class="text-text-secondary block mb-2">Теги:</span>

                  <div v-if="tagsLoading" class="text-sm text-text-secondary">
                    Загрузка тегов...
                  </div>

                  <div v-else class="flex flex-wrap items-center gap-2">
                    <template v-if="availableTags?.length">
                      <div
                        v-for="tag in availableTags"
                        :key="tag.id"
                        class="group relative flex items-center gap-2"
                      >
                        <label class="cursor-pointer flex items-center gap-2">
                          <input
                            type="checkbox"
                            :value="tag.id"
                            v-model="selectedTagIds"
                            class="w-4 h-4 accent-accent"
                          />
                          <span class="border border-accent text-accent rounded-full px-3 py-1 text-sm">
                            {{ tag.name }}
                          </span>
                        </label>

                        <!-- КРЕСТИК ПРИ НАВЕДЕНИИ -->
                        <button
                          type="button"
                          @click.stop="openDeleteTagModal(tag)"
                          class="absolute -bottom-1 right-0 w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity shadow"
                          title="Удалить тег"
                        >
                          ×
                        </button>
                      </div>
                    </template>

                    <!-- Кнопка "+ в кружочке" -->
                    <button
                      type="button"
                      @click="openAddTagModal"
                      class="ml-2 w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center text-lg hover:bg-opacity-90 transition-opacity"
                      title="Добавить новый тег"
                    >
                      +
                    </button>
                  </div>

                  <div v-if="!tagsLoading && (!availableTags || availableTags.length === 0)" class="text-sm text-text-secondary">
                    Нет доступных тегов
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-2">
            <button class="btn w-full" @click="saveChanges">Добавить питомца</button>
            <button class="secondary-btn w-full" @click="cancelAdd">Отменить</button>
          </div>
        </div>
      </main>
    </div>

    <!-- МОДАЛЬНОЕ ОКНО: СОЗДАНИЕ ТЕГА -->
    <Modal
      v-if="isAddTagModalOpen"
      title="Создать тег"
      :is-open="isAddTagModalOpen"
      @close="closeAddTagModal"
    >
      <div class="flex flex-col gap-4 p-4">
        <div>
          <label class="block text-text-secondary mb-2">Название тега</label>
          <input
            v-model="newTagName"
            type="text"
            class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
            placeholder="Например: Дружелюбный"
            @keyup.enter="createNewTag"
          />
          <span v-if="newTagError" class="text-error text-sm mt-1">Поле не может быть пустым</span>
        </div>

        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeAddTagModal">Отмена</button>
          <button class="btn" @click="createNewTag">Создать</button>
        </div>
      </div>
    </Modal>

    <!-- МОДАЛЬНОЕ ОКНО: УДАЛЕНИЕ ТЕГА -->
    <Modal
      v-if="isDeleteTagModalOpen"
      title="Удалить тег"
      :is-open="isDeleteTagModalOpen"
      @close="closeDeleteTagModal"
    >
      <div class="flex flex-col gap-4 p-4">
        <p>
          Удалить тег «<strong>{{ tagToDelete?.name }}</strong>»?
        </p>
        <p class="text-sm text-text-secondary">
          Это действие нельзя отменить. Убедитесь, что тег не используется.
        </p>

        <span v-if="deleteTagError" class="text-error text-sm">{{ deleteTagError }}</span>

        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeDeleteTagModal">Отмена</button>
          <button class="btn" @click="confirmDeleteTag">Удалить</button>
        </div>
      </div>
    </Modal>
  </section>
</template>