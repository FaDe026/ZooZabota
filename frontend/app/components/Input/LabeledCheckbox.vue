<script lang="ts" setup>
const { name = "" } = defineProps<{
    name?: string
}>()
</script>
<template>
    <label class="flex gap-2 items-center text-text-secondary">
        <input class="checkbox" type="checkbox" :name="name">
        <slot></slot>
    </label>
</template>