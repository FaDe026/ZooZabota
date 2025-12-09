<script lang="ts" setup>
definePageMeta({
    layout: "admin"
})

</script>
<template>
    <section class="h-[calc(100vh-200px)] py-10 flex flex-col justify-between px-4 gap-4">
        <div class="flex flex-col gap-4">
            <div class="flex text-xl flex-col gap-1 text-text-primary">
                <span>Новые заявки: 2</span>
                <span>Животные в приюте: 124</span>
                <span>Требуют внимания: 4</span>
            </div>
            <div class="flex flex-col gap-2">
                <a href="" class="card-bg card-shadow py-4 text-center rounded-xl text-2xl">Заявки</a>
                <a href="" class="card-bg card-shadow py-4 text-center rounded-xl text-2xl">Животные</a>
                <a href="" class="card-bg card-shadow py-4 text-center rounded-xl text-2xl">Новости</a>
            </div>
        </div>
        <button class="btn w-min self-center">Выйти</button>
    </section>
</template>