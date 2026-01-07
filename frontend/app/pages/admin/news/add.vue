<script lang="ts" setup>
definePageMeta({
  layout: "admin"
})

import { apiFetch } from "~/composables/useAPI"
import { useTags } from '~/composables/useTags'

type Tag = { id: number; name: string }

const router = useRouter()

const editTitle = ref("")
const editBody = ref("")
const editPreview = ref("")
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)
const selectedTagIds = ref<number[]>([])
const { data: availableTags, pending: tagsLoading } = useTags<Tag[]>()
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

    selectedTagIds.value = selectedTagIds.value.filter(id => id !== tagToDelete.value!.id)

    closeDeleteTagModal()
  } catch (e: any) {
    deleteTagError.value = e.response?.data?.detail || "Невозможно удалить тег"
  }
}
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

async function saveNews() {
  const titleError = !editTitle.value.trim()
  const bodyError = !editBody.value.trim()

  if (titleError || bodyError) {
    return
  }

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
    await apiFetch("/news", {
      method: "POST",
      body: formData
    })
    router.back()
  } catch (e) {
    console.error("Ошибка добавления новости:", e)
  }
}

function cancelAdd() {
  router.back()
}
</script>

<template>
  <section class="flex flex-col gap-4 base-section">
    <div class="base-container mx-auto relative flex justify-center items-center mb-2">
      <svg
        class="absolute left-0 cursor-pointer"
        @click="backClicked()"
        width="55"
        height="47"
        viewBox="0 0 55 47"
        fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <path
          d="M43.5416 23.5H11.4583"
          stroke="#1A3C40"
          stroke-width="5"
          stroke-linecap="round"
          stroke-linejoin="round"/>
        <path
          d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166"
          stroke="#1A3C40"
          stroke-width="5"
          stroke-linecap="round"
          stroke-linejoin="round"/>
      </svg>

      <h1 class="text-2xl text-primary text-center font-bold">Добавить новость</h1>
    </div>

    <div class="min-h-screen bg-bg font-cuprum">
      <main class="base-section pt-10">
        <div class="flex flex-col gap-2 mx-auto base-container">
          <div class="flex justify-center">
            <div class="card-bg rounded-2xl overflow-hidden shadow-lg border border-gray-200 w-full">
              <div
                class="w-full h-96 bg-gray-200 flex items-center justify-center overflow-hidden relative">
                <img v-if="previewImage" :src="previewImage" alt="Предпросмотр" class="w-full h-full object-cover" />
                <Icon v-else name="mdi:newspaper" class="text-6xl text-text-secondary" />

                <div
                  class="absolute inset-0 bg-black/20 bg-opacity-50 flex items-center justify-center cursor-pointer"
                  @click="triggerImageUpload">
                  <button type="button" class="btn text-xl pointer-events-none">
                    {{ previewImage ? 'Изменить изображение' : 'Добавить изображение' }}
                  </button>
                </div>
                <input type="file" id="imageInput" accept="image/*" class="hidden" @change="handleImageChange" />
              </div>

              <div class="p-6">
                <div class="mb-4">
                  <TextInput v-model="editTitle" placeholder="Заголовок новости" />
                  <span v-if="!editTitle.trim()" class="text-error text-sm">Заголовок не может быть пустым</span>
                </div>
                <div class="mb-4">
                  <div
                    class="border-2 border-input-border px-4 py-3 rounded-xl focus-within:border-accent transition-colors">
                    <input
                      v-model="editPreview"
                      type="text"
                      placeholder="Краткое описание (необязательно)"
                      class="focus:outline-0 w-full text-text-secondary"/>
                  </div>
                </div>
                <div class="mb-6">
                  <div
                    class="border-2 border-input-border px-4 py-3 rounded-xl focus-within:border-accent transition-colors">
                    <textarea
                      v-model="editBody"
                      placeholder="Текст новости"
                      rows="6"
                      class="focus:outline-0 w-full text-text-secondary resize-none">
                    </textarea>
                  </div>
                  <span v-if="!editBody.trim()" class="text-error text-sm">Текст не может быть пустым</span>
                </div>
              </div>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row gap-2">
            <button class="btn w-full" @click="saveNews">Добавить новость</button>
            <button class="secondary-btn w-full" @click="cancelAdd">Отменить</button>
          </div>
        </div>
      </main>
    </div>
  </section>
</template>