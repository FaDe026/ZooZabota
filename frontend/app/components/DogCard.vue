<script lang="ts" setup>
import { DogGender } from '~/types/dogGender';

const config = useRuntimeConfig()

const { dog } = defineProps<{
    dog: Dog
}>()

const emit = defineEmits<{
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
function openCustodyModal() {
    emit('openCustodyModal')
}

function openTakeModal() {
    emit('openTakeModal')
}
</script>
<template>
    <div
        class="bg-linear-to-b from-white to-[#F9F7F2] rounded-2xl overflow-hidden shadow-lg border border-gray-200 cursor-pointer transition-transform hover:scale-105 duration-300">
        <div
            class="w-full h-64 bg-gray-200 flex items-center justify-center overflow-hidden  rounded-bl-xl rounded-br-xl">
            <img v-if="hasImage" :src="imageUrl" :alt="dog.name" class="w-full h-full object-cover" lazyload>
            <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />
        </div>

        <div class="p-6">
            <h3 class="section-title flex justify-center items-center">{{ dog.name }}</h3>

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
        </div>

        <div class="flex flex-col md:flex-row gap-2 md:gap-3 p-6 pt-0">
            <button class="btn text-xl font-normal flex-1" @click.stop="openTakeModal()">
                ХОЧУ ЗАБРАТЬ
            </button>
            <button
                class="btn text-xl bg-transparent border-2 border-accent text-accent font-normal flex-1 hover:bg-accent hover:text-white transition-colors"
                @click.stop="openCustodyModal()">
                ВЗЯТЬ ПОД ОПЕКУ
            </button>
        </div>
    </div>
</template>