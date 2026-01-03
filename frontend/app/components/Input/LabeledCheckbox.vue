<script lang="ts" setup>
const { name = "", postion = "before" } = defineProps<{
    name?: string
    postion?: "before" | "after"
}>()

const model = defineModel<boolean>({ default: false })
</script>
<template>
    <label class="flex gap-2 items-center text-text-secondary">
        <input v-if="postion === 'before'" class="checkbox" type="checkbox" :name="name" v-model="model">
        <slot></slot>
        <input v-if="postion === 'after'" class="checkbox" type="checkbox" :name="name" v-model="model">
    </label>
</template>