<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})

import { apiFetch } from "~/composables/useAPI"
import { useTags } from '~/composables/useTags'

type Tag = { id: number; name: string }

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()

const { data: newsData, pending, error } = await useServerFetch<News>(
  `/news/${String(route.params.id)}`
)


const { data: tagsData, pending: tagsLoading } = await useTags<Tag[]>()

const news = ref(newsData.value)
const availableTags = ref(tagsData.value)

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

const isInEditMode = ref(false)
const editTitle = ref("")
const editBody = ref("")
const editPreview = ref("")
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)
const selectedTagIds = ref<string[]>([])
const titleError = ref(false)
const bodyError = ref(false)
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

watch(news, (newNews) => {
  if (newNews?.image_url) {
    previewImage.value = newNews.image_url
  } else {
    previewImage.value = null
  }
}, { immediate: true })

function backClicked() {
  router.back()
}

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

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '—'
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = String(date.getFullYear()).slice(-2)
  return `${day}.${month}.${year}`
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
      <svg
        class="absolute left-0 cursor-pointer"
        @click="backClicked"
        width="55"
        height="47"
        viewBox="0 0 55 47"
        fill="none"
        xmlns="http://www.w3.org/2000/svg">
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
                class="w-full h-full object-cover"/>
              <Icon
                v-else
                name="mdi:newspaper"
                class="absolute inset-0 m-auto text-6xl text-text-secondary"/>
              <div
                v-if="isInEditMode"
                class="absolute inset-0 bg-black/30 flex items-center justify-center cursor-pointer"
                @click="triggerImageUpload">
                <button class="btn text-xl pointer-events-none">Изменить изображение</button>
              </div>
              <input
                id="imageInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageChange"/>
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
                    class="border-2 border-accent text-accent rounded-full px-4 py-1 text-sm">
                    {{ tag.name }}
                  </span>
                </div>
              </div>

              <div v-else class="mb-6 text-text-secondary">
                <div class="mb-4">
                  <input
                    v-model="editTitle"
                    type="text"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
                    placeholder="Заголовок новости"/>
                  <span v-if="titleError" class="text-error text-sm">Заголовок не может быть пустым</span>
                </div>
                <div class="mb-4">
                  <input
                    v-model="editPreview"
                    type="text"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent"
                    placeholder="Краткое описание (необязательно)"
                  />
                </div>

                <div class="mb-4">
                  <textarea
                    v-model="editBody"
                    rows="6"
                    class="w-full border border-input-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent resize-none"
                    placeholder="Текст новости">
                  </textarea>
                  <span v-if="bodyError" class="text-error text-sm">Текст не может быть пустым</span>
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
  </section>
</template>