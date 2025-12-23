<script lang="ts" setup>
import { DogGender } from '~/types/dogGender';


const { dog, isOpen } = defineProps<{
    isOpen: boolean,
    dog: Dog
}>()

const emit = defineEmits<{
    (e: 'close'): void,
    (e: 'openTakeModal'): void,
    (e: 'openCustodyModal'): void,
}>()

const gender = computed(() => {
    return (dog.gender === DogGender.male) ? "Мужской" : "Женский"
})
const veterinaryPassport = computed(() => {
    return (dog.vetirinary_passport) ? "есть" : "нет"
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
</script>
<template>
    <Modal :is-open="isOpen" @close="close()">
        <div class="card-bg rounded-2xl overflow-hidden shadow-lg border border-gray-200 w-full mx-9">
            <div class="w-full h-96 bg-gray-200 flex items-center justify-center overflow-hidden">
                <img v-if="dog.image" :src="dog.image" :alt="dog.name" class="w-full h-full object-cover">
                <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />
            </div>

            <div class="p-6">
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
                    <span v-for="tag in dog.tags" :key="tag"
                        class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1">
                        {{ tag }}
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