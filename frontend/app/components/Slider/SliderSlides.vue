<script lang="ts" setup>

const { count, slideClass = "" } = defineProps<{
    count: number,
    slideClass?: string,
}>()

const emit = defineEmits<{
    (e: 'currentSlideUpdate', index: number): void
}>()

const slidesRef = useTemplateRef('slides')
const slidesBaseRef = useTemplateRef('slidesBase')

let innerSlide = 0
const currentSlide = defineModel<number>({ default: 0 })

let slideObserver: IntersectionObserver | null = null

function updateCurrentSlide(newSlide: HTMLElement) {
    if (!slidesRef.value) {
        return
    }
    for (const [index, slide] of slidesRef.value.entries()) {
        if (slide === newSlide) {
            innerSlide = index
            emit('currentSlideUpdate', index)
            break
        }
    }
}

watch(currentSlide, (newValue) => {
    if (!slidesRef.value || !slidesBaseRef.value) {
        return
    }
    if (newValue >= count || newValue === innerSlide) {
        return
    }
    const slide = slidesRef.value[newValue]
    if (slide) {
        slidesBaseRef.value.scrollBy({
            left: slide.getBoundingClientRect().left,
            behavior: "smooth",
        })
    }
})

onMounted(() => {
    if (import.meta.client && slidesBaseRef.value && slidesRef.value) {
        const observer = new IntersectionObserver((entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    updateCurrentSlide(entry.target as HTMLElement)
                }
            }
        }, {
            root: slidesBaseRef.value,
            threshold: 0.9,
            rootMargin: "0px",
        })

        slideObserver = observer

        slidesRef.value.forEach((slide) => {
            observer.observe(slide)
        })
    }
})

</script>
<template>
    <div class="flex gap-1 w-full py-2 overflow-x-scroll h-full snap-x snap-mandatory" ref="slidesBase">
        <div v-for="index in count" class="w-[90%] shrink-0 snap-center" ref="slides" :class="slideClass" :key="index">
            <slot :index="index - 1"></slot>
            <!-- {{ (slidesRef) ? slidesRef[index - 1]?.getBoundingClientRect().left : "" }} -->
        </div>
    </div>
</template>