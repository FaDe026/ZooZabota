<script lang="ts" setup>
/**
* Крч не самым лучшим образом реализовал компонент.
* Перепишу через стандартное <component :is ="..."> 
*/

const { currentTab } = defineProps<{
    currentTab: number,
}>()

const mainDiv = useTemplateRef('stepperTabs')
let prevCurrent = currentTab

const divChildren = [] as HTMLElement[]

watch(() => currentTab, (newVal) => {
    if (divChildren.length === 0) {
        return
    }
    const index = clamp(newVal, 0, divChildren.length - 1)
    const child = divChildren[index]
    const prevChild = divChildren[prevCurrent]
    if (child && prevChild && (index != prevCurrent)) {
        child.style.display = "block"
        prevChild.style.display = "none"
        prevCurrent = index
    }
},)

onMounted(() => {
    if (mainDiv.value) {
        const children = mainDiv.value.children
        for (let i = 0; i < children.length; i++) {
            const child = children[i]
            if (child instanceof HTMLElement) {
                divChildren.push(child)
                if (i != (currentTab)) {
                    child.style.display = "none"
                }
            }
        }
    }
})

</script>

<template>
    <div ref="stepperTabs" class="stack grid grid-cols-1 grid-rows-1">
        <slot></slot>
    </div>
</template>

<style lang="postcss">
.stack {
    >* {
        grid-area: 1 / 1;
    }
}
</style>