<script lang="ts" setup>

const config = useRuntimeConfig()

const { date = '12.10.25', title = 'Новость', imgSrc = '', newsId = '404' } = defineProps<{
    date?: string,
    title?: string,
    imgSrc?: string | null,
    newsId?: string,
}>()

const imageUrl = computed(() => {
    return `${config.public.apiBase}${imgSrc}`
})

const hasImage = computed(() => {
    return (imgSrc) ? true : false
})
const titleProcessed = computed(() => title.replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('\n', '<br />'))

</script>
<template>
    <NuxtLink class="flex flex-col gap-2 w-full cursor-pointer" :to="`/news/${newsId}`">
        <span class="text-text-muted-bg ">{{ date }}</span>
        <div
            class="flex bg-gray-200 items-center justify-center w-full aspect-video object-cover rounded-xl shadow-xl/10 self-center overflow-hidden">
            <img v-if="hasImage" class="object-cover w-full h-full" :src="imageUrl" alt="">
            <Icon v-else name="material-symbols:newspaper" class="text-6xl text-text-secondary" />
        </div>
        <h3 class="text-2xl text-primary">{{ title }}</h3>
    </NuxtLink>
</template>