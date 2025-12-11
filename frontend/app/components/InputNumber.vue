<script lang="ts" setup>
const { min = 0 } = defineProps<{
    max?: number
    min?: number
}>()

const counter = defineModel<number>({ default: 0 })

function decreaseClicked() {
    counter.value = Math.max(min, counter.value - 1)
}


function increaseClicked() {
    counter.value = counter.value + 1
}

</script>
<template>
    <div class="flex items-center gap-3">
        <button class="h-min p-2 border border-input-border rounded-md text-text-secondary text-2xl/2 cursor-pointer"
            @click.prevent="decreaseClicked">
            -
        </button>
        <span class="text-text-secondary">{{ counter }}</span>
        <button class="h-min p-2 border border-input-border rounded-md text-text-secondary text-2xl/2 cursor-pointer"
            @click.prevent="increaseClicked">
            +
        </button>
    </div>
</template>