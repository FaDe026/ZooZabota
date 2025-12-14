<script lang="ts" setup>
const { pageActiveColorClass = "bg-pagination-active", pageInactiveColorClass = "bg-pagination-inactive" } = defineProps<{
    pageCount: number
    pageActiveColorClass?: string
    pageInactiveColorClass?: string
}>()

const currentPage = defineModel<number>({ default: 0 })
const emit = defineEmits<{
    (e: 'pageClicked', page: number): void
}>()

function pageColor(page: number) {
    return (page === currentPage.value) ? pageActiveColorClass : pageInactiveColorClass
}

function pageClicked(page: number) {
    emit('pageClicked', page)
}

</script>
<template>
    <div class="flex gap-2">
        <div v-for="page in pageCount" class="rounded-full w-3 h-3 cursor-pointer" :class="pageColor(page)" @click="pageClicked(page)">
        </div>
    </div>
</template>