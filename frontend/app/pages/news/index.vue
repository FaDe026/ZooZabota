<script lang="ts" setup>

const { data: newsList, error, pending: pendingNews } = useServerFetch<News[]>(`/news`)

const isNewsListEmpty = computed(() => {
    return newsList.value && newsList.value.length === 0
})

const isErrorPresent = computed(() => {
    return error.value !== undefined
})

watch(error, () => {
    console.log("asdfasdfasfasdf")
    console.log(error.value)
})

</script>
<template>
    <section class="base-section">
        <h1 class="text-2xl text-primary text-center font-bold mb-7">Новости приюта</h1>
        <div class="base-container mx-auto flex justify-center items-center w-full h-100 text-text-secondary text-center text-2xl"
            v-if="isNewsListEmpty">
            Новостей пока нет!
        </div>
        <div class="base-container mx-auto flex justify-center items-center w-full h-100 text-alert text-center text-2xl"
            v-else-if="isErrorPresent">
            Произошла ошибка при загрузке новостей.<br>Приносим свои извнения! =(
        </div>
        <div class="base-container mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 w-full gap-5" v-else>
            <NewsCard v-for="news in newsList" img-src="/images/news/1.png" :title="news.title" :key="news.id"
                :news-id="`${news.id}`" :date="news.date"></NewsCard>
        </div>
    </section>
</template>