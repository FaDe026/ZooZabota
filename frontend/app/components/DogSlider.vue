<script lang="ts" setup>
interface DogSlide {
    name: string,
    imgSrc: string
}

const dogSlides = [
    {
        name: "Арчи",
        imgSrc: "/"
    },
    {
        name: "Тоби",
        imgSrc: "/"
    },
    {
        name: "asdasd",
        imgSrc: "/"
    },
] as DogSlide[]

const currentPage = ref(0)
const changeSlideModel = ref(0)

function currentSlideUpdate(index: number) {
    currentPage.value = index
}


function changeSlide(index: number) {
    changeSlideModel.value = index
}

</script>
<template>
    <div class="flex flex-col gap-2 items-center justify-center w-full">
        <SliderSlides :count="dogSlides.length" v-slot="slotProps" @current-slide-update="currentSlideUpdate"
            v-model="changeSlideModel">
            <div class="flex items-center justify-center w-full h-60 border border-primary rounded-2xl">
                {{ dogSlides[slotProps.index]?.name }}
            </div>
        </SliderSlides>
        <SliderPagination :page-count="dogSlides.length" v-model="currentPage"
            @page-clicked="changeSlide($event - 1)"></SliderPagination>
    </div>
</template>