<template>
    <Modal :is-open="isOpen" @close="closeModal()" modal-class="py-3 w-full sm:max-w-md" :level="level"
        title="Взять под опеку">
        <div class=" sm:min-w-sm px-3">
            <form @submit.prevent="submitForm" class="space-y-2">
                <div>
                    <label class="block text-text-secondary mb-1 text-sm pl-3">Фамилия Имя Отчество</label>
                    <input v-model="formData.fullName" type="text" required
                        class="w-full px-4 py-3 border-2 border-input-border rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                        placeholder="Иванов Иван Иванович">
                </div>
                <div>
                    <label class="block text-text-secondary mb-1 text-sm pl-3">Телефон</label>
                    <input v-model="formData.phone" type="tel" required
                        class="w-full px-4 py-3 border-2 border-input-border rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                        placeholder="+7 (900) 000-00-00">
                </div>
                <div>
                    <label class="block text-text-secondary mb-1 text-sm pl-3">Email</label>
                    <input v-model="formData.email" type="email" required
                        class="w-full px-4 py-3 border-2 border-input-border rounded-xl focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent text-text-primary text-sm"
                        placeholder="i.ivanov123@mail.ru">
                </div>
                <div class="flex gap-3 pt-4">
                    <button type="submit"
                        class="px-6 py-3 bg-accent text-white rounded-xl hover:bg-opacity-90 transition-colors text-lg mx-auto block">
                        Отправить
                    </button>
                </div>
            </form>
        </div>
    </Modal>
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
    level: number
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

const closeModal = () => {
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
})
</script>
