<script lang="ts" setup>

const { current } = defineProps<{
    count: number,
    current: number
}>()

function getBg(stepNumber: number) {
    return ((stepNumber - 1) <= current) ? "bg-accent" : "bg-text-secondary"
}

</script>
<template>

    <div class="flex gap-0.5 w-full py-2 px-6">
        <div class="h-1.5 rounded-2xl w-full" v-for="num in count" :class="getBg(num)"></div>
    </div>

</template>