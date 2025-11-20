<script lang="ts" setup>

const test = ref('Помочь приюту')

</script>

<template>
    <header class="w-full bg-primary text-bg flex justify-center">
        <div class="w-full">
            <div class="flex justify-between items-center w-full px-10 py-5">
                <h1 class="uppercase text-7xl tracking-wider">Ковчег</h1>
                <button class="btn" @click="test = 'А зачем ты сюда нажал(-a)?'">{{ test }}</button>
            </div>
            <nav class="flex justify-evenly w-full">
                <a href="" class="nav-btn border-l-0">Наши питомцы</a>
                <a href="" class="nav-btn">Приют</a>
                <a href="" class="nav-btn">Новости</a>
                <a href="" class="nav-btn">Контакты</a>
            </nav>
        </div>
    </header>
</template>