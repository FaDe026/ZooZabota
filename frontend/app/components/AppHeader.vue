<script lang="ts" setup>

const navExpanded = ref(false)

const navClasses = computed(() => {
    return { 'nav--expanded': navExpanded.value }
})

function hamburgerClicked() {
    navExpanded.value = !navExpanded.value
}

</script>

<template>
    <header class="sticky sm:relative top-0 z-20 w-full bg-primary text-bg flex justify-center">
        <div class="w-full">
            <div class="flex justify-between items-center w-full px-5 py-5">
                <h1 class="uppercase text-4xl sm:text-7xl tracking-wider">Ковчег</h1>
                <button class="btn hidden sm:block">Помочь приюту</button>
                <button class="sm:hidden" @click="hamburgerClicked()">
                    <div class="flex flex-col gap-2 w-10 " v-if="!navExpanded">
                        <span class="h-1 bg-bg rounded-sm"></span>
                        <span class="h-1 bg-bg rounded-sm"></span>
                        <span class="h-1 bg-bg rounded-sm"></span>
                    </div>
                    <Icon class="w-10 text-[40px]" name="mage:multiply" v-else></Icon>
                </button>
            </div>
            <nav :class="navClasses"
                class="flex flex-col justify-evenly w-full max-h-0 transition-[max-height] duration-350 overflow-hidden divide-hidden sm:max-h-200 sm:flex-row sm:divide-solid sm:divide-x divide-nav-border">
                <a href="/ourPets" class="nav-btn">Наши питомцы</a>
                <a href="" class="nav-btn">Приют</a>
                <a href="" class="nav-btn">Новости</a>
                <a href="" class="nav-btn">Контакты</a>
            </nav>
        </div>
    </header>
</template>

<style lang="postcss">
.nav--expanded {
    max-height: 800px;
}
</style>