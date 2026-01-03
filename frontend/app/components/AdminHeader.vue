<template>
    <header class="sticky sm:relative top-0 z-20 w-full bg-primary text-bg flex justify-center">
        <div class="w-full">
            <div class="flex justify-center items-center w-full px-5 py-5">
                <NuxtLink to="/admin">
                    <img width="55" height="55" class="object-cover brightness-0 invert-100" src="/images/logo.png"
                        alt="Логотип">
                </NuxtLink>
            </div>
        </div>
    </header>
</template>

<style lang="postcss">
.nav--expanded {
    max-height: 800px;
}
</style>