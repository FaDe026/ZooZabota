<script lang="ts" setup>

const { isOpen } = defineProps<{
    isOpen: boolean
}>()

const currentTab = ref(0)
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
}

watch(() => isOpen, (newVal) => {
    if (!newVal) {
        currentTab.value = 0
    }
})

</script>

<template>
    <Modal @close="closeModal" title="Забрать друга" :is-open="isOpen">
        <template #beforeHeader>
            <Stepper :count="3" :current="currentTab"></Stepper>
        </template>
        <div class="flex flex-col gap-2 px-6 pt-2 pb-6">
            <h3 class="text-text-secondary text-center">Заполните небольшую анкету,<br>чтобы записаться на встречу с
                питомцем</h3>
            <StepperTabs :current-tab="currentTab">
                <div class="flex flex-col gap-1">
                    <label for="name" class="text-text-secondary">Фамилия имя</label>
                    <TextInput input-id="name" placeholder="Иван Иванов" class="mb-2"></TextInput>

                    <label for="phoneInput" class="text-text-secondary">Телефон</label>
                    <TextInput input-id="phoneInput" placeholder="+7 (800) 55-35-34" class="mb-2"></TextInput>

                    <label for="emailInput" class="text-text-secondary">E-mail</label>
                    <TextInput input-id="emailInput" placeholder="i.ivanov123@mail.ru" class="mb-2"></TextInput>
                </div>
                <div>
                    test2
                </div>
                <div>
                    test3
                </div>
                <div>
                    test4
                </div>
            </StepperTabs>
            <div class="flex gap-2 justify-center">
                <button class="secondary-btn text-2xl" @click="prevTab()" v-show="showBackBtn">Назад</button>
                <button class="btn text-2xl" @click="nextBtnClick()">
                    {{ nextBtnText }}
                </button>
            </div>
        </div>
    </Modal>
</template>