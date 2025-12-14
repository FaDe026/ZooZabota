<script lang="ts" setup>

const { placeholder = "", name = "", inputId = "", type = "text" } = defineProps<{
    placeholder?: string
    name?: string
    inputId?: string
    type?: string
}>()

const model = defineModel<string>()
const inputRef = useTemplateRef('input')

function focusInput() {
    if (inputRef.value) {
        inputRef.value.focus()
    }
}

</script>

<template>
    <div class="border border-input-border px-4 py-2 rounded-lg hover:cursor-text" @click="focusInput">
        <input :type="type" :id="inputId" :name="name" ref="input" v-model="model" :placeholder="placeholder"
            class="focus:outline-0 w-full text-text-secondary">
    </div>
</template>
