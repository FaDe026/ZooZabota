<script lang="ts" setup>

const config = useRuntimeConfig()
interface DogSlide {
    id: number,
    image_url: string
}



const { data: slides, pending } = useServerFetch<DogSlide[]>("/dogs/random")

const currentPage = ref(0)
const changeSlideModel = ref(0)

const slidesLoaded = computed(() => {
    return (slides.value !== undefined)
})

function currentSlideUpdate(index: number) {
    currentPage.value = index
}


function changeSlide(index: number) {
    changeSlideModel.value = index
}

</script>
<template>
    <div class="flex flex-col gap-2 items-center justify-center w-full">
        <div v-if="pending"
            class="flex justify-center items-center w-full aspect-video border border-primary text-text-primary rounded-2xl">
            <span class="text-center text-2xl">Загружаем питомцев...</span>
        </div>
        <template v-else-if="slides">
            <SliderSlides :count="slides.length" v-slot="slotProps" @current-slide-update="currentSlideUpdate"
                v-model="changeSlideModel">
                <div class="flex items-center justify-center w-full aspect-video  rounded-2xl overflow-hidden">
                    <img class="object-cover h-full w-full"
                        :src="`${config.public.apiBase}${slides[slotProps.index]?.image_url}`" lazyload>
                </div>
            </SliderSlides>
            <SliderPagination :page-count="slides.length" v-model="currentPage" @page-clicked="changeSlide($event - 1)">
            </SliderPagination>
        </template>
        <div v-else
            class="flex justify-center items-center w-full aspect-video border border-primary text-text-primary rounded-2xl">
            <span class="text-center text-2xl">Возникли проблемы при загрузке питомцев.<br>Приносим свои
                извинения!</span>
        </div>
    </div>
</template>