<script setup lang="ts">

const emit = defineEmits<{
    (e: 'close'): void
}>()

const { isOpen, title = "Заголовок", modalClass = "", headerClass = "" } = defineProps<{
    isOpen: boolean,
    title?: string,
    modalClass?: string,
    headerClass?: string
}>()

function closeModal() {
    emit('close')
}

function disableBodyScroll() {
    document.body.style.overflow = 'hidden'
}

function enableBodyScroll() {
    document.body.style.overflow = ''
}

function clickedOutside() {
    emit('close')
}

watch(() => isOpen, (newVal) => {
    if (newVal) {
        disableBodyScroll()
    } else {
        enableBodyScroll()
    }
})

</script>

<template>
    <Transition name="modal-transition">
        <div v-if="isOpen" class="fixed inset-0 bg-primary/40 flex items-center justify-center z-50 p-4"
            @click="clickedOutside">
            <div class="bg-linear-to-t from-card-bottom-color to-card-top-color rounded-2xl shadow-lg max-w-md w-full"
                :class="modalClass" @click.stop>
                <slot name="beforeHeader"></slot>
                <div class="flex items-center justify-center relative px-6" :class="headerClass">
                    <h2 class="text-xl font-medium text-center">{{ title }}</h2>
                    <button @click="closeModal"
                        class="absolute right-6 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-primary transition-colors">
                        <Icon name="material-symbols:close" class="text-3xl" />
                    </button>
                </div>
                <slot></slot>
            </div>
        </div>
    </Transition>
</template>

<style>
.modal-transition-enter-active,
.modal-transition-leave-active {
    transition: transform 150ms ease, opacity 150ms ease;
}

.modal-transition-enter-from,
.modal-transition-leave-to {
    opacity: 0;
    transform: scale(1.2);
}
</style>