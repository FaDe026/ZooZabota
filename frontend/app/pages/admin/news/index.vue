<script lang="ts" setup>
definePageMeta({
  layout: 'admin'
})

const router = useRouter()
const {   data: newsList, error, pending } = useServerFetch<News[]>('/news')

const isNewsListEmpty = computed(() => {
  return Array.isArray(newsList.value) && newsList.value.length === 0
})

const isErrorPresent = computed(() => {
  return error.value !== undefined
})

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '—'

  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = String(date.getFullYear()).slice(-2)

  return `${day}.${month}.${year}`
}

function getPreview(news: News): string {
  if (news.preview) return news.preview
  return news.body.length > 100 ? news.body.substring(0, 100) + '...' : news.body
}

function backClicked() {
  router.back()
}
</script>

<template>
  <section class="flex flex-col gap-4 base-section">
    <div class="base-container mx-auto relative flex justify-center items-center mb-2">
      <svg
        class="absolute left-0 cursor-pointer"
        @click="backClicked()"
        width="55"
        height="47"
        viewBox="0 0 55 47"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M43.5416 23.5H11.4583"
          stroke="#1A3C40"
          stroke-width="5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166"
          stroke="#1A3C40"
          stroke-width="5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <h1 class="text-2xl text-primary text-center font-bold">Новости</h1>
    </div>

    <div class="base-container flex mx-auto">
      <NuxtLink to="/admin/news/add" class="btn w-full">Добавить новость</NuxtLink>
    </div>

    <div v-if="pending" class="base-container mx-auto text-center text-text-secondary">
      Загрузка...
    </div>

    <div v-else-if="isErrorPresent" class="base-container mx-auto text-center text-red-500">
      Ошибка загрузки новостей
    </div>

    <div v-else-if="isNewsListEmpty" class="base-container mx-auto text-center text-text-secondary">
      Нет новостей
    </div>

    <div v-else class="flex flex-col gap-2 base-container mx-auto">
      <div
        v-for="news in newsList"
        :key="news.id"
        class="flex card-bg card-shadow rounded-xl px-4 py-2"
      >
        <div class="flex flex-col grow">
          <h2 class="text-text-primary text-xl mb-1">{{ news.title }}</h2>
          <p class="text-text-secondary text-sm mb-2">
            {{ getPreview(news) }}
          </p>
          <div class="text-text-tertiary text-xs text-right mt-2">
            {{ formatDate(news.date) }}
          </div>
        </div>
        <div class="flex items-center">
          <NuxtLink :href="`/admin/news/${news.id}`" class="btn px-6 w-fit">Просмотр</NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>