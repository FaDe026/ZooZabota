<script lang="ts" setup>
const { name = "", value = "", postion = "before" } = defineProps<{
    name?: string,
    value?: any,
    postion?: "before" | "after"
}>()

const model = defineModel()
</script>
<template>
    <label class="flex gap-2 items-center text-text-secondary">
        <input v-if="postion === 'before'" class="radio" type="radio" :name="name" v-model="model" :value="value">
        <slot></slot>
        <input v-if="postion === 'after'" class="radio" type="radio" :name="name" v-model="model" :value="value">
    </label>
</template>