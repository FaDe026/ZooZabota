<script lang="ts" setup>
definePageMeta({
    layout: "admin"
})
import { DogGender } from '~/types/dogGender'

const router = useRouter()
const config = useRuntimeConfig()

// Данные формы
const editName = ref("")
const editDescription = ref("")
const editTags = ref<string[]>([])
const newTag = ref("")
const editAge = ref<number>(0)
const editGender = ref<DogGender>(DogGender.male)
const editVetPassport = ref(false)
const selectedImage = ref<File | null>(null)
const previewImage = ref<string | null>(null)

// Валидация
const nameError = ref(false)
const descriptionError = ref(false)
const ageError = ref(false)
const tagErrors = ref<boolean[]>([])

function backClicked() {
    router.back()
}

function addTag() {
    const trimmedTag = newTag.value.trim()
    if (trimmedTag && !editTags.value.includes(trimmedTag)) {
        editTags.value.push(trimmedTag)
        tagErrors.value.push(false)
        newTag.value = ""
    }
}

function removeTag(index: number) {
    editTags.value.splice(index, 1)
    tagErrors.value.splice(index, 1)
}

function handleImageChange(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
        selectedImage.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
            previewImage.value = e.target?.result as string
        }
        reader.readAsDataURL(file)
    }
}

function triggerImageUpload() {
    const input = document.getElementById('imageInput') as HTMLInputElement
    input?.click()
}

async function saveChanges() {
    nameError.value = !editName.value.trim()
    descriptionError.value = !editDescription.value.trim()
    ageError.value = editAge.value <= 0 || isNaN(editAge.value)

    tagErrors.value = editTags.value.map(tag => !tag.trim())
    const hasEmptyTags = tagErrors.value.some(error => error)

    if (nameError.value || descriptionError.value || ageError.value || hasEmptyTags) {
        return
    }

    try {
        const formData = new FormData()
        formData.append('name', editName.value.trim())
        formData.append('description', editDescription.value.trim())
        formData.append('age', editAge.value.toString())
        formData.append('gender', editGender.value)
        formData.append('vetirinary_passport', editVetPassport.value.toString())
        formData.append('tags', JSON.stringify(editTags.value.map(tag => tag.trim())))

        if (selectedImage.value) {
            formData.append('image', selectedImage.value)
        }

        // await $fetch(`${config.public.apiBase}/dogs`, {
        //     method: "POST",
        //     body: formData
        // })

        console.log('Питомец добавлен:', {
            name: editName.value.trim(),
            description: editDescription.value.trim(),
            age: editAge.value,
            gender: editGender.value,
            vetirinary_passport: editVetPassport.value,
            tags: editTags.value.map(tag => tag.trim()),
            image: selectedImage.value
        })

        router.back()
    } catch (err) {
        console.error('Ошибка добавления:', err)
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

                                <div class="flex flex-wrap gap-2 mb-6">
                                    <div v-for="(tag, index) in editTags" :key="index"
                                        class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1 flex items-center gap-2">
                                        {{ tag }}
                                        <button type="button" @click="removeTag(index)"
                                            class="text-accent hover:text-red-500 transition-colors">
                                            ✕
                                        </button>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <button type="button" @click="addTag"
                                            class="btn text-xl rounded-full px-4 py-1">
                                            Добавить тэг
                                        </button>
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
    </section>
</template>