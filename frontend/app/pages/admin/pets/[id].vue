<script lang="ts" setup>
definePageMeta({
    layout: "admin"
})
import { FetchError } from 'ofetch';
import { DogGender } from '~/types/dogGender'


const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()
const { data: dog, error, pending } = useServerFetch<Dog>(`/dogs/${route.params.id}`)

const isDeleteModalOpen = ref(false)
const deleteMessage = ref<string | null>(null);
const deleteStatus = ref<"none" | "success" | "error">("none")

const isInEditMode = ref(false)

// Редактируемые данные
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

const gender = computed(() => {
    if (!dog.value) return ""
    return (dog.value.gender === DogGender.male) ? "Мужской" : "Женский"
})

const veterinaryPassport = computed(() => {
    if (!dog.value) return ""
    return (dog.value.veterinary_passport) ? "есть" : "нет"
})

const age = computed(() => {
    return ageText(dog.value)
})

const displayDeleteMessage = computed(() => {
    return deleteStatus.value !== "none"
})

const deleteMessageClasses = computed(() => {
    return {
        "text-success": (deleteStatus.value === "success"),
        "text-error": (deleteStatus.value === "error"),
    }
})

const displayImage = computed(() => {
    if (previewImage.value) return previewImage.value
    return dog.value?.image
})

function closeDeleteModal() {
    isDeleteModalOpen.value = false
    deleteStatus.value = "none"
}

function openDeleteModal() {
    isDeleteModalOpen.value = true
}

async function deleteDog() {
    if (!dog.value) return
    try {
        await $fetch(`${config.public.apiBase}/dogs/${dog.value.id}`, { method: "DELETE" })
        deleteMessage.value = "Животное удалено успешно!"
        deleteStatus.value = "success"
        setTimeout(() => router.back(), 500)
    }
    catch (err) {
        deleteMessage.value = "Не удалось удалить животное, произошла ошибка. Приносим свои извинения."
        console.log(err)
        deleteStatus.value = "error"
    }
}

function backClicked() {
    router.back()
}

function toggleEditMode() {
    if (!dog.value) return

    if (!isInEditMode.value) {
        // Входим в режим редактирования
        editName.value = dog.value.name
        editDescription.value = dog.value.description
        // editTags.value = [...dog.value.tags]
        editTags.value = []
        editAge.value = dog.value.age
        editGender.value = dog.value.gender
        editVetPassport.value = dog.value.veterinary_passport
        nameError.value = false
        descriptionError.value = false
        ageError.value = false
        tagErrors.value = []
        previewImage.value = null
        selectedImage.value = null
    }
    console.log(dog.value)
    isInEditMode.value = !isInEditMode.value
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

function updateTagValue(index: number, value: string) {
    editTags.value[index] = value
    // Проверка на пустоту при обновлении
    tagErrors.value[index] = !value.trim()
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
    // Валидация
    nameError.value = !editName.value.trim()
    descriptionError.value = !editDescription.value.trim()
    ageError.value = editAge.value <= 0 || isNaN(editAge.value)

    // Проверка тегов на пустоту
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

        // await $fetch(`${config.public.apiBase}/dogs/${dog.value?.id}`, {
        //     method: "PATCH",
        //     body: formData
        // })

        console.log('Сохранение:', {
            name: editName.value.trim(),
            description: editDescription.value.trim(),
            age: editAge.value,
            gender: editGender.value,
            vetirinary_passport: editVetPassport.value,
            tags: editTags.value.map(tag => tag.trim()),
            image: selectedImage.value
        })

        if (dog.value) {
            // dog.value.name = editName.value.trim()
            // dog.value.description = editDescription.value.trim()
            // dog.value.age = editAge.value
            // dog.value.gender = editGender.value
            // dog.value.veterinary_passport = editVetPassport.value
            // console.log(gender.value)
            // dog.value.tags = editTags.value.map(tag => tag.trim())
            // if (previewImage.value) {
            //     dog.value.image = previewImage.value
            // }
            dog.value = {
                ...dog.value,
                name: editName.value.trim(),
                description: editDescription.value.trim(),
                age: editAge.value,
                gender: editGender.value,
                veterinary_passport: editVetPassport.value,
                tags: editTags.value.map(tag => tag.trim()),
                image: previewImage.value ?? dog.value.image
            }
        }

        isInEditMode.value = false
    } catch (err) {
        console.error('Ошибка сохранения:', err)
    }
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

            <h1 class="text-2xl text-primary text-center font-bold">Животные</h1>
        </div>
        <div class="min-h-screen bg-bg font-cuprum">
            <main class="base-section pt-10">
                <div class="flex flex-col gap-2 mx-auto base-container">
                    <div v-if="dog" class="flex justify-center">
                        <div class="card-bg rounded-2xl overflow-hidden shadow-lg border border-gray-200 w-full">
                            <div
                                class="w-full h-96 bg-gray-200 flex items-center justify-center overflow-hidden relative">
                                <img v-if="displayImage" :src="displayImage" :alt="dog.name"
                                    class="w-full h-full object-cover">
                                <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />

                                <div v-if="isInEditMode"
                                    class="absolute inset-0 bg-black/20 bg-opacity-50 flex items-center justify-center cursor-pointer"
                                    @click="triggerImageUpload">
                                    <button type="button" class="btn text-xl pointer-events-none">Изменить
                                        фотографию</button>
                                </div>
                                <input type="file" id="imageInput" accept="image/*" class="hidden"
                                    @change="handleImageChange">
                            </div>

                            <div class="p-6">
                                <!-- Имя собаки -->
                                <div v-if="isInEditMode" class="mb-4">
                                    <TextInput v-model="editName" placeholder="Имя собаки" />
                                    <span v-if="nameError" class="text-error text-sm">Имя не может быть пустым</span>
                                </div>
                                <h3 v-else class="section-title flex justify-center items-center mb-4">{{ dog.name }}
                                </h3>

                                <!-- Описание -->
                                <div class="mb-6">
                                    <div v-if="isInEditMode">
                                        <div
                                            class="border-2 border-input-border px-4 py-3 rounded-xl focus-within:border-accent transition-colors">
                                            <textarea v-model="editDescription" placeholder="Описание" rows="4"
                                                class="focus:outline-0 w-full text-text-secondary resize-none"></textarea>
                                        </div>
                                        <span v-if="descriptionError" class="text-error text-sm">Описание не может быть
                                            пустым</span>
                                    </div>
                                    <p v-else class="text-xl text-text-primary leading-relaxed">
                                        {{ dog.description }}
                                    </p>
                                </div>

                                <!-- Информация о собаке -->
                                <div v-if="isInEditMode" class="flex flex-col gap-4 mb-6">
                                    <!-- Пол -->
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

                                    <!-- Возраст -->
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

                                    <!-- Ветпаспорт -->
                                    <div>
                                        <LabeledCheckbox postion="after" name="vetPassport" v-model="editVetPassport">
                                            Ветпаспорт:
                                        </LabeledCheckbox>
                                    </div>
                                </div>
                                <div v-else class="flex flex-col gap-2 mb-4">
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Пол: {{ gender }}</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Возраст: {{ age }}</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Ветпаспорт: {{ veterinaryPassport }}</span>
                                    </div>
                                </div>

                                <div v-if="isInEditMode" class="flex flex-wrap gap-2 mb-6">
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
                                <div v-else class="flex flex-wrap gap-2 mb-6">
                                    <span v-for="tag in dog.tags" :key="tag"
                                        class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1">
                                        {{ tag }}
                                    </span>
                                </div>

                            </div>
                        </div>
                    </div>
                    <div v-else class="text-center py-20">
                        <p class="text-2xl text-text-secondary">Собака не найдена</p>
                    </div>

                    <div v-if="!isInEditMode" class="flex flex-col sm:flex-row gap-2">
                        <button class="btn w-full" @click="toggleEditMode">Редактировать карточку</button>
                        <button class="secondary-btn w-full" @click="openDeleteModal()">Удалить карточку</button>
                    </div>
                    <div v-else class="flex flex-col sm:flex-row gap-2">
                        <button class="btn w-full" @click="saveChanges">Сохранить изменения</button>
                        <button class="secondary-btn w-full" @click="toggleEditMode">Отменить</button>
                    </div>

                    <Modal title="Удаление карточки" :is-open="isDeleteModalOpen" @close="closeDeleteModal()">
                        <template #beforeHeader>
                            <div class="w-full h-4"></div>
                        </template>
                        <div class="flex flex-col gap-2 p-4">
                            <span class="text-text-secondary">
                                Вы уверены, что хотите удалить карточку "{{ dog?.name }}"?
                            </span>
                            <span class="" v-if="displayDeleteMessage" :class="deleteMessageClasses">
                                {{ deleteMessage }}
                            </span>
                            <div class="flex justify-evenly gap-3">
                                <button class="secondary-btn text-xl" @click="closeDeleteModal()">Оставить</button>
                                <button class="btn text-xl" @click="deleteDog()">Удалить</button>
                            </div>
                        </div>
                    </Modal>
                </div>
            </main>
        </div>
    </section>
</template>