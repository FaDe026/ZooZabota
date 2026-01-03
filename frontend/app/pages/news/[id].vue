<script lang="ts" setup>
const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()

const { data: news, error, pending } = useServerFetch<News>(`/news/${route.params.id}`)

const imageUrl = computed(() => {
    if (!news.value) return ""
    return `${config.public.apiBase}${news.value.image_url}`
})

const hasImage = computed(() => {
    if (!news.value) return false
    return (news.value.image_url) ? true : false
})

function backClicked() {
    router.back()
}

</script>
<template>
    <section class="base-section">
        <div class="base-container mx-auto relative flex justify-center items-center mb-7">
            <svg class="absolute left-0 cursor-pointer" @click="backClicked()" width="55" height="47"
                viewBox="0 0 55 47" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round"
                    stroke-linejoin="round" />
                <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
                    stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <h1 class="text-2xl text-primary text-center font-bold">{{ news?.title }}</h1>
        </div>
        <div class="base-container flex flex-col gap-3 mx-auto">
            <div
                class="flex bg-gray-200 items-center justify-center w-full aspect-video object-cover rounded-xl shadow-xl/10 self-center overflow-hidden">
                <img v-if="hasImage" class="object-cover w-full h-full" :src="imageUrl" alt="">
                <Icon v-else name="material-symbols:newspaper" class="text-6xl text-text-secondary" />
            </div>
            <div class="text-text-primary text-xl">
                {{ news?.body }}
            </div>
        </div>
    </section>
</template>