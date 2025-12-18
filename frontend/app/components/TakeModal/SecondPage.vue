<template>
    <div class="flex flex-col gap-2">
        <div class="flex flex-col gap-1">
            <span class="text-text-secondary">Сколько человек в семье?</span>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="peopleInFamilyCount" class="radio">
                Я один/одна
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="peopleInFamilyCount" class="radio">
                Семья с детьми
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="peopleInFamilyCount" class="radio">
                Пара
            </label>
        </div>
        <div class="flex flex-col gap-1">
            <span class="text-text-secondary">Был ли у Вас опыт содержания животных ранее?</span>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                Это будет первый питомец
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                Ранее были кошки/ собаки
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                На данный момент имеются животные в семье
            </label>
        </div>
        <div class="flex flex-col gap-1">
            <span class="text-text-secondary">С какой целью берете питомца?</span>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petGoal" class="radio">
                Для себя
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petGoal" class="radio">
                В подарок
            </label>
        </div>
    </div>
</template>