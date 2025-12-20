<script lang="ts" setup>

const { date = '12.10.25', title = 'Новость', imgSrc = '', newsId = '404' } = defineProps<{
    date?: string,
    title?: string,
    imgSrc?: string,
    newsId?: string,
}>()

const titleProcessed = computed(() => title.replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('\n', '<br />'))

</script>
<template>
    <NuxtLink class="flex flex-col gap-2 w-full cursor-pointer" :to="`/news/${newsId}`">
        <span class="text-text-muted-bg ">{{ date }}</span>
        <img class="w-full aspect-video object-cover rounded-xl shadow-xl/10" :src="imgSrc" alt="">
        <h3 class="text-2xl text-primary">{{ title }}</h3>
    </NuxtLink>
</template>