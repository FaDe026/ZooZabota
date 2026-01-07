<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})

import { apiFetch } from "~/composables/useAPI"
import { useTags } from '~/composables/useTags'

// Явное определение типа тега (обход ошибки в types.d.ts)
type Tag = { id: number; name: string }

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()

// Загрузка новости - исправлена деструктуризация
const { data: newsData, pending, error } = await useAsyncData<News>(
  `news-${route.params.id}`,
  () => apiFetch(`/news/${String(route.params.id)}`)
)

// Загрузка тегов - исправлена деструктуризация
const { data: tagsData, pending: tagsLoading } = await useTags<Tag[]>()

// Реактивные ссылки для удобства
const news = ref(newsData.value)
const availableTags = ref(tagsData.value)

// Удаление новости
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

async function deleteNews() {
  if (!news.value) return
  try {
    await apiFetch(`/news/${news.value.id}`, { method: "DELETE" })
    deleteMessage.value = "Новость удалена успешно!"
    deleteStatus.value = "success"
    setTimeout(() => router.back(), 500)
  } catch {
    deleteMessage.value = "Ошибка удаления"
    deleteStatus.value = "error"
  }
}

// Редактирование
const isInEditMode = ref(false)

const editTitle = ref("")
const editBody = ref("")
const editPreview = ref("")
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)
const selectedTagIds = ref<string[]>([])

const titleError = ref(false)
const bodyError = ref(false)

// Модалки для тегов
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

// Вычисляемые свойства
const displayDeleteMessage = computed(() =>
  deleteStatus.value !== "none"
)

const deleteMessageClasses = computed(() => ({
  "text-success": deleteStatus.value === "success",
  "text-error": deleteStatus.value === "error"
}))

// Инициализация при загрузке новости
watch(news, (newNews) => {
  if (newNews?.image_url) {
    previewImage.value = newNews.image_url
  } else {
    previewImage.value = null
  }
}, { immediate: true })

// Навигация
function backClicked() {
  router.back()
}

// Переключение режима редактирования
function toggleEditMode() {
  if (!news.value) return

  if (!isInEditMode.value) {
    editTitle.value = news.value.title
    editBody.value = news.value.body
    editPreview.value = news.value.preview || ""
    selectedTagIds.value = news.value.tags?.map((t: Tag) => t.id.toString()) || []
    selectedImage.value = null
  }
  isInEditMode.value = !isInEditMode.value
}

// Работа с изображением
function triggerImageUpload() {
  document.getElementById("imageInput")?.click()
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

// Сохранение изменений
async function saveChanges() {
  if (!news.value) return

  titleError.value = !editTitle.value.trim()
  bodyError.value = !editBody.value.trim()

  if (titleError.value || bodyError.value) return

  const formData = new FormData()
  formData.append("title", editTitle.value.trim())
  formData.append("body", editBody.value.trim())
  if (editPreview.value.trim()) {
    formData.append("preview", editPreview.value.trim())
  }

  formData.append("tag_ids", selectedTagIds.value.join(","))

  if (selectedImage.value) {
    formData.append("file", selectedImage.value)
  }

  try {
    const updated = await apiFetch<News>(
      `/news/${news.value.id}`,
      { method: "PATCH", body: formData }
    )
    news.value = updated
    isInEditMode.value = false
  } catch (e) {
    console.error("Ошибка сохранения", e)
  }
}

// Форматирование даты
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '—'
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = String(date.getFullYear()).slice(-2)
  return `${day}.${month}.${year}`
}

// Получение полного URL изображения
function getImageUrl(path: string | null): string | undefined {
  if (!path) return undefined
  if (path.startsWith('data:')) return path
  return `${config.public.apiBase}${path}`
}
</script>

<template>
  <section class="flex flex-col gap-4 base-section">
    <div class="base-container mx-auto relative flex justify-center items-center mb-2">
      <svg
        class="absolute left-0 cursor-pointer"
        @click="backClicked"
        width="55"
        height="47"
        viewBox="0 0 55 47"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round" />
        <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
          stroke-linecap="round" />
      </svg>
      <h1 class="text-2xl text-primary font-bold">Новости</h1>
    </div>

    <div v-if="pending" class="text-center py-20 text-xl">Загрузка..</div>
    <div v-else-if="error" class="text-center py-20 text-error text-xl">Ошибка загрузки</div>
    <div v-else-if="news" class="min-h-screen bg-bg font-cuprum">
      <main class="base-section pt-10">
        <div class="base-container mx-auto">
          <div class="card-bg rounded-2xl overflow-hidden shadow-lg">
            <div class="w-full h-96 bg-gray-200 relative">
              <img
                v-if="previewImage"
                :src="getImageUrl(previewImage)"
                :alt="news.title"
                class="w-full h-full object-cover"
              />
              <Icon
                v-else
                name="mdi:newspaper"
                class="absolute inset-0 m-auto text-6xl text-text-secondary"
              />
              <div
                v-if="isInEditMode"
                class="absolute inset-0 bg-black/30 flex items-center justify-center cursor-pointer"
                @click="triggerImageUpload"
              >
                <button class="btn text-xl pointer-events-none">Изменить изображение</button>
              </div>
              <input
                id="imageInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageChange"
              />
            </div>

            <div class="p-6">
              <h2 class="section-title text-center mb-2">
                {{ news.title }}
              </h2>
              <p class="text-text-secondary text-sm text-center mb-4">
                {{ formatDate(news.date) }}
              </p>

              <div v-if="!isInEditMode" class="mb-6">
                <div v-if="news.preview" class="mb-3 text-text-primary text-lg">
                  <p>{{ news.preview }}</p>
                </div>
                <div class="mb-4 text-text-primary text-lg whitespace-pre-line">
                  <p>{{ news.body }}</p>
                </div>
                <div v-if="news.tags && news.tags.length > 0" class="flex flex-wrap gap-2 mb-6">
                  <span
                    v-for="tag in news.tags"
                    :key="tag.id"
                    class="border-2 border-accent text-accent rounded-full px-4 py-1 text-sm"
                  >
                    {{ tag.name }}
                  </span>
                </div>
              </div>

              <div v-else class="mb-6 text-text-secondary">
                <!-- Заголовок -->
                <div class="mb-4">
                  <input
                    v-model="editTitle"
                    type="text"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
                    placeholder="Заголовок новости"
                  />
                  <span v-if="titleError" class="text-error text-sm">Заголовок не может быть пустым</span>
                </div>

                <!-- Краткое описание -->
                <div class="mb-4">
                  <input
                    v-model="editPreview"
                    type="text"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
                    placeholder="Краткое описание (необязательно)"
                  />
                </div>

                <!-- Основной текст -->
                <div class="mb-4">
                  <textarea
                    v-model="editBody"
                    rows="6"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent resize-none"
                    placeholder="Текст новости"
                  ></textarea>
                  <span v-if="bodyError" class="text-error text-sm">Текст не может быть пустым</span>
                </div>

                <!-- Теги -->
                <div class="mb-6">
                  <div v-if="tagsLoading" class="text-sm text-text-secondary">Загрузка тегов..</div>
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
                            :value="tag.id.toString()"
                            v-model="selectedTagIds"
                            class="sr-only peer"
                          />
                          <span
                            class="relative overflow-hidden border rounded-full px-5 py-3 pr-9 text-base font-medium transition-colors duration-150"
                            :class="selectedTagIds.includes(tag.id.toString())
                              ? 'text-accent border-accent border-2'
                              : 'text-text-secondary border-gray-300 border-2'"
                          >
                            {{ tag.name }}
                          </span>
                        </label>
                        <button
                          type="button"
                          @click.stop="openDeleteTagModal(tag)"
                          class="absolute top-1/2 right-2 -translate-y-1/2 w-5 h-5 rounded-full bg-transparent text-accent flex items-center justify-center opacity-0 translate-x-4 group-hover:opacity-100 group-hover:translate-x-0 hover:bg-red-500 hover:text-white transition-all duration-200 ease-out"
                          title="Удалить тег"
                        >
                          <svg
                            viewBox="0 0 24 24"
                            class="w-3.5 h-3.5"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.75"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
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
                      title="Добавить новый тег"
                    >
                      +
                    </button>
                  </div>
                  <div
                    v-if="!tagsLoading && (!availableTags || availableTags.length === 0)"
                    class="text-sm text-text-secondary"
                  >
                    Нет доступных тегов
                  </div>
                </div>
              </div>

              <!-- Кнопки -->
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

    <!-- Модалка удаления новости -->
    <Modal
      title="Удаление новости"
      :is-open="isDeleteModalOpen"
      @close="closeDeleteModal"
    >
      <div class="flex flex-col gap-4 p-4">
        <span>Удалить новость «{{ news?.title }}»?</span>
        <span v-if="displayDeleteMessage" :class="deleteMessageClasses">
          {{ deleteMessage }}
        </span>
        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeDeleteModal">Отмена</button>
          <button class="btn" @click="deleteNews">Удалить</button>
        </div>
      </div>
    </Modal>

    <!-- Модалка создания тега -->
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
            placeholder="Например: Важное"
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

    <!-- Модалка удаления тега -->
    <Modal
      v-if="isDeleteTagModalOpen"
      title="Удалить тег"
      :is-open="isDeleteTagModalOpen"
      @close="closeDeleteTagModal"
    >
      <div class="flex flex-col gap-4 p-4">
        <p>Удалить тег «{{ tagToDelete?.name }}»?</p>
        <p class="text-sm text-text-secondary">
          Это действие нельзя отменить. Убедитесь, что тег не используется.
        </p>
        <span v-if="deleteTagError" class="text-accent text-sm">{{ deleteTagError }}</span>
        <div class="flex gap-3 justify-end">
          <button class="secondary-btn" @click="closeDeleteTagModal">Отмена</button>
          <button class="btn" @click="confirmDeleteTag">Удалить</button>
        </div>
      </div>
    </Modal>
  </section>
</template>