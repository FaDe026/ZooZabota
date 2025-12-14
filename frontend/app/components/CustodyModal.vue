<template>
    <div v-if="isOpen" class="fixed inset-0 bg-primary/40 flex items-center justify-center z-50 p-4">
        <div class="bg-linear-to-t from-card-bottom-color to-card-top-color rounded-2xl shadow-lg max-w-md w-full">
            <div class="px-6 pt-4">
                <div class="relative">
                    <h2 class="text-xl font-cuprum font-medium text-center">Взять под опеку</h2>
                    <button 
                        @click="closeModal"
                        class="absolute right-0 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-primary transition-colors">
                        <Icon name="material-symbols:close" class="text-3xl" />
                    </button>
                </div>
            </div>

            <div class="p-3 ">
                <form @submit.prevent="submitForm" class="space-y-2">
                    <div>
                        <label class="block text-text-secondary mb-1 text-sm pl-3">Фамилия Имя Отчество</label>
                        <input 
                            v-model="formData.fullName"
                            type="text" 
                            required
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                            placeholder="Иванов Иван Иванович"
                        >
                    </div>
                    <div>
                        <label class="block text-text-secondary mb-1 text-sm pl-3">Телефон</label>
                        <input 
                            v-model="formData.phone"
                            type="tel" 
                            required
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                            placeholder="+7 (900) 000-00-00"
                        >
                    </div>
                    <div>
                        <label class="block text-text-secondary mb-1 text-sm pl-3">Email</label>
                        <input 
                            v-model="formData.email"
                            type="email" 
                            required
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                            placeholder="i.ivanov123@mail.ru"
                        >
                    </div>
                    <div class="flex gap-3 pt-4">
                        <button 
                            type="submit"
                            class="px-6 py-3 bg-accent text-white rounded-xl hover:bg-opacity-90 transition-colors text-lg mx-auto block">
                            Отправить
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
interface Dog {
    id: number
    name: string
    image?: string
}

interface Props {
    isOpen: boolean
    dog?: Dog
}

interface Emits {
    (e: 'close'): void
    (e: 'submit', data: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const formData = reactive({
    fullName: '',
    phone: '',
    email: ''
})

const disableBodyScroll = () => {
    document.body.style.overflow = 'hidden'
}

const enableBodyScroll = () => {
    document.body.style.overflow = ''
}

const closeModal = () => {
    enableBodyScroll()
    emit('close')
}

const submitForm = () => {
    const formDataWithDog = {
        ...formData,
        dog: props.dog
    }
    emit('submit', formDataWithDog)
    formData.fullName = ''
    formData.phone = ''
    formData.email = ''
    
    closeModal()
}
watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        disableBodyScroll()
    } else {
        enableBodyScroll()
    }
})

const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && props.isOpen) {
        closeModal()
    }
}

onMounted(() => {
    document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
    document.removeEventListener('keydown', handleEscape)
    enableBodyScroll() 
})
</script>

