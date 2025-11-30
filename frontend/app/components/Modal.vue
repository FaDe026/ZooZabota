<script setup lang="ts">

const emit = defineEmits<{
    (e: 'close'): void
}>()

const { isOpen, title = "Заголовок" } = defineProps<{
    isOpen: boolean,
    title?: string
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

function clickedOutside(){
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
    <div v-if="isOpen" class="fixed inset-0 bg-primary/40 flex items-center justify-center z-50 p-4" @click="clickedOutside">
        <div class="bg-linear-to-t from-card-bottom-color to-card-top-color rounded-2xl shadow-lg max-w-md w-full py-4" @click.stop>
            <slot name="beforeHeader"></slot>
            <div class="px-6">
                <div class="relative">
                    <h2 class="text-xl font-medium text-center">{{ title }}</h2>
                    <button @click="closeModal"
                        class="absolute right-0 top-1/2 transform -translate-y-1/2 text-text-secondary hover:text-primary transition-colors">
                        <Icon name="material-symbols:close" class="text-3xl" />
                    </button>
                </div>
            </div>
            <slot></slot>
        </div>
    </div>
</template>