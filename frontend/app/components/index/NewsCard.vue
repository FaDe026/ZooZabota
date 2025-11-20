<script lang="ts" setup>

const { date = '12.10.25', title = 'Новость', imgSrc = '' } = defineProps<{
    date?: string,
    title?: string,
    imgSrc?: string
}>()

const titleProcessed = computed(()=> title.replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('\n', '<br />'))

</script>
<template>
    <div class="flex flex-col gap-2 w-full">
        <span class="text-text-muted-bg ">{{ date }}</span>
        <img class="w-full aspect-video object-cover rounded-4xl" :src="imgSrc" alt="">
        <h3 class="text-2xl text-primary">{{ title }}</h3>
    </div>
</template>