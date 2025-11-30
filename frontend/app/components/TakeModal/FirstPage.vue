<template>
    <div class="flex flex-col gap-1">
        <label for="name" class="text-text-secondary">Фамилия имя</label>
        <TextInput input-id="name" placeholder="Иван Иванов" class="mb-2"></TextInput>

        <label for="phoneInput" class="text-text-secondary">Телефон</label>
        <TextInput input-id="phoneInput" placeholder="+7 (800) 55-35-34" class="mb-2"></TextInput>

        <label for="emailInput" class="text-text-secondary">E-mail</label>
        <TextInput input-id="emailInput" placeholder="i.ivanov123@mail.ru" class="mb-2"></TextInput>
    </div>
</template>