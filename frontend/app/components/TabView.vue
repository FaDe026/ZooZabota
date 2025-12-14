<script lang="ts" setup>
/**
* Крч не самым лучшим образом реализовал компонент.
* Перепишу через стандартное <component :is ="..."> 
*/

const { currentTab, tabs } = defineProps<{
    currentTab: number,
    tabs: Component[]
}>()

const current = ref(tabs[0])

watch(() => currentTab, (newVal) => {
    const index = clamp(newVal, 0, tabs.length - 1)
    current.value = tabs[index]
},)

onMounted(() => {
    if (tabs.length === 0) {
        return
    }
    const index = clamp(currentTab, 0, tabs.length - 1)
    current.value = tabs[currentTab]
})

</script>

<template>
    <div ref="stepperTabs" class="stack grid grid-cols-1 grid-rows-1">
        <component :is="current"></component>
    </div>
</template>

<style lang="postcss">
.stack {
    >* {
        grid-area: 1 / 1;
    }
}
</style>