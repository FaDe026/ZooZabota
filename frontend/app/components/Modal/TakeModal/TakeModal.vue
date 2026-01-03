<script lang="ts" setup>

import { TakeModalFirstPage, TakeModalSecondPage, TakeModalFourthPage, TakeModalThirdPage } from "#components"
import { baseModalProps } from "~/shared/props/modalProps";

const { isOpen } = defineProps(baseModalProps)

const currentTab = ref(0)
const isNotLastTab = computed(() => {
    return currentTab.value !== 3
})

const tabs = ref([
    markRaw(TakeModalFirstPage),
    markRaw(TakeModalSecondPage),
    markRaw(TakeModalThirdPage),
    markRaw(TakeModalFourthPage),
])

const showBackBtn = computed(() => {
    return currentTab.value > 0
})


const nextBtnText = computed(() => {
    return (currentTab.value < 3) ? "Далее" : "Ок"
})

const emit = defineEmits<{
    (e: 'close'): void
}>()

function closeModal() {
    emit('close')
}

function nextTab() {
    currentTab.value = Math.min(3, currentTab.value + 1)
}

function prevTab() {
    currentTab.value = Math.max(0, currentTab.value - 1)
}

function nextBtnClick() {
    if (currentTab.value < 3) {
        nextTab()
    }
    else {
        closeModal()
    }
}

watch(() => isOpen, (newVal) => {
    if (!newVal) {
        currentTab.value = 0
    }
})

</script>

<template>
    <Modal @close="closeModal" title="Забрать друга" :is-open="isOpen" :level="level" modal-class="w-full sm:max-w-md">
        <template #beforeHeader>
            <Stepper :count="3" :current="currentTab"></Stepper>
        </template>
        <div class="flex flex-col gap-2 px-6 pt-2 pb-6">
            <h3 class="text-text-secondary text-center" v-if="isNotLastTab">Заполните небольшую анкету,<br>чтобы
                записаться
                на
                встречу с
                питомцем</h3>
            <TabView :current-tab="currentTab" :tabs="tabs"></TabView>
            <div class="flex gap-2 justify-center">
                <button class="secondary-btn text-2xl" @click="prevTab()" v-show="showBackBtn">Назад</button>
                <button class="btn text-2xl" @click="nextBtnClick()">
                    {{ nextBtnText }}
                </button>
            </div>
        </div>
    </Modal>
</template>