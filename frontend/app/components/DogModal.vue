<script lang="ts" setup>
import type { PropType } from 'vue';
import { baseModalProps } from '~/shared/props/modalProps';
import { DogGender } from '~/types/dogGender';


const config = useRuntimeConfig()

const { dog, isOpen } = defineProps({
    ...baseModalProps,
    dog: {
        required: true,
        type: Object as PropType<Dog>
    }
})

const emit = defineEmits<{
    (e: 'close'): void,
    (e: 'openTakeModal'): void,
    (e: 'openCustodyModal'): void,
}>()

const gender = computed(() => {
    return (dog.gender === DogGender.male) ? "Мужской" : "Женский"
})
const veterinaryPassport = computed(() => {
    return (dog.veterinary_passport) ? "есть" : "нет"
})

const imageUrl = computed(() => {
    return `${config.public.apiBase}${dog.image_url}`
})

const hasImage = computed(() => {
    return (dog.image_url) ? true : false
})

function close() {
    emit('close')
}

function openCustodyModal() {
    emit('openCustodyModal')
}

function openTakeModal() {
    emit('openTakeModal')
}

watch(() => dog, (newVal) => {
    console.log("changed to ", dog)
})

</script>
<template>
    <Modal :is-open="isOpen" @close="close()" modal-class="w-full sm:max-w-xl" :has-header="false">
        <div class="flex flex-col relative card-bg rounded-2xl overflow-hidden w-full">
            <div class="absolute right-2 top-2 cursor-pointer" @click="close()">
                <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M30 10L10 30" stroke="url(#paint0_linear_426_315)" stroke-width="4.5"
                        stroke-linecap="round" stroke-linejoin="round" />
                    <path d="M10 10L30 30" stroke="url(#paint1_linear_426_315)" stroke-width="4.5"
                        stroke-linecap="round" stroke-linejoin="round" />
                    <defs>
                        <linearGradient id="paint0_linear_426_315" x1="20" y1="10" x2="20" y2="30"
                            gradientUnits="userSpaceOnUse">
                            <stop stop-color="white" />
                            <stop offset="1" stop-color="#F9F7F2" />
                        </linearGradient>
                        <linearGradient id="paint1_linear_426_315" x1="20" y1="10" x2="20" y2="30"
                            gradientUnits="userSpaceOnUse">
                            <stop stop-color="white" />
                            <stop offset="1" stop-color="#F9F7F2" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <div
                class="w-full aspect-video bg-gray-200 flex items-center justify-center overflow-hidden rounded-bl-xl rounded-br-xl">
                <img v-if="hasImage" :src="imageUrl" :alt="dog.name" class="w-full h-full object-cover">
                <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />
            </div>

            <div class="flex flex-col p-6">
                <h3 class="section-title flex justify-center items-center mb-4">{{ dog.name }}</h3>
                <div class="mb-6">
                    <p class="text-xl text-text-primary leading-relaxed">
                        {{ dog.description }}
                    </p>
                </div>
                <div class="flex flex-col gap-2 mb-4">
                    <div class="flex items-center">
                        <span class="text-text-secondary">Пол: {{ gender }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-text-secondary">Возраст: {{ dog.age }}</span>
                    </div>
                    <div class="flex items-center">
                        <span class="text-text-secondary">Ветпаспорт: {{ veterinaryPassport }}</span>
                    </div>
                </div>

                <div class="flex flex-wrap gap-2 mb-6">
                    <span v-for="tag in dog.tags" :key="tag.id"
                        class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1">
                        {{ tag.name }}
                    </span>
                </div>

                <div class="flex flex-col md:flex-row gap-2 md:gap-3">
                    <button class="btn text-xl font-normal flex-1" @click="openTakeModal">
                        ХОЧУ ЗАБРАТЬ
                    </button>
                    <button @click="openCustodyModal"
                        class="btn text-xl bg-transparent border-2 border-accent text-accent font-normal flex-1 hover:bg-accent hover:text-white transition-colors">
                        ВЗЯТЬ ПОД ОПЕКУ
                    </button>
                </div>
            </div>
        </div>
    </Modal>
</template>