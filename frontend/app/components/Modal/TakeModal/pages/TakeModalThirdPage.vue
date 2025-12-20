<template>
    <div class="flex flex-col gap-2">
        <div class="flex flex-col gap-1">
            <span class="text-text-secondary">Ваши жилищные условия</span>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="liveConditions" class="radio">
                Арендую жилье
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="liveConditions" class="radio">
                Квартира
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="liveConditions" class="radio">
                Частный дом
            </label>
        </div>
        <div class="flex flex-col gap-1">
            <span class="text-text-secondary">Размер жилья</span>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                До 40 м2
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                40-60 м2
            </label>
            <label class="flex items-center gap-2 text-text-secondary">
                <input type="radio" name="petExperience" class="radio">
                Более 60 м2
            </label>
        </div>
    </div>
</template>