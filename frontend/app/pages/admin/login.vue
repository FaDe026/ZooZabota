<script lang="ts" setup>
definePageMeta({
    layout: "admin"
})
</script>

<template>
    <section class="flex flex-col justify-center items-center px-2 h-[calc(100vh-200px)] w-full">
        <h1 class="text-center text-4xl text-text-primary mb-6">КОВЧЕГ</h1>
        <form action="" class="flex flex-col gap-3 w-full max-w-100">
            <TextInput placeholder="Логин" class="input-grad-bg border-0 shadow-lg"></TextInput>
            <TextInput placeholder="Пароль" type="password" class="input-grad-bg border-0 shadow-lg"></TextInput>
            <label class="text-text-secondary flex items-center gap-2 px-4">
                <input type="checkbox" class="checkbox">
                Я не робот(честн честно)
            </label>
            <button class="btn">Войти</button>
            <a href="#" class="self-center text-text-secondary">Забыли пароль?</a>
        </form>
    </section>
</template>