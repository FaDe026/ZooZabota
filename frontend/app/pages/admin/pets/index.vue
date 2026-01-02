<script lang="ts" setup>
definePageMeta({
    layout: "admin"
})

const router = useRouter()

function backClicked() {
    router.back()
}
</script>

<template>
    <section class="flex flex-col gap-4 base-section">
        <div class="base-container mx-auto relative flex justify-center items-center mb-2">
            <svg class="absolute left-0 cursor-pointer" @click="backClicked()" width="55" height="47"
                viewBox="0 0 55 47" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round"
                    stroke-linejoin="round" />
                <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
                    stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <h1 class="text-2xl text-primary text-center font-bold">Животные</h1>
        </div>

        <div class="base-container mx-auto">
            <button class="btn w-full">Добавить животное</button>
        </div>

        <div class="flex flex-col gap-2 base-container mx-auto">
            <div class="flex card-bg card-shadow rounded-xl px-4 py-2">
                <div class="flex flex-col grow">
                    <h2 class="text-text-primary text-xl mb-1">Марс</h2>
                    <div class="flex flex-col text-text-secondary">
                        <span>Пол: Мужской</span>
                        <span>Возраст: 2 года</span>
                        <span>Наличие ветпаспорта: есть</span>
                    </div>
                </div>
                <div class="flex items-center">
                    <button class="btn px-6 w-fit">Просмотр</button>
                </div>
            </div>
        </div>
    </section>
</template>