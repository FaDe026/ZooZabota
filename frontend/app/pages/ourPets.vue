<template>
    <div class="min-h-screen bg-bg font-cuprum">
        <main class="base-section pt-10">
            <div class="mx-auto base-container">
                <h1 class="section-title text-center mb-8">Наши питомцы</h1>
                
                <!-- Кнопка открытия фильтров -->
                <div class="flex justify-end mb-8">
                    <button class="font-cuprum text-text-secondary flex items-center gap-3 px-12 py-3 cursor-pointer">
                        <span class="text-xl">Фильтры</span>
                        <Icon name="material-symbols:keyboard-arrow-down" class="text-2xl" />
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div 
                        v-for="dog in dogs" 
                        :key="dog.id" 
                        class="pet-card"
                    >
                        <div class="pet-image">
                            <img 
                                v-if="dog.image" 
                                :src="dog.image" 
                                :alt="dog.name" 
                                class="w-full h-full object-cover"
                            >
                            <Icon 
                                v-else 
                                name="material-symbols:pets" 
                                class="text-6xl text-text-secondary" 
                            />
                        </div>
                        
                        <div class="pet-content">
                            <h3 class="section-title flex justify-center items-center">{{ dog.name }}</h3>
                            
                            <div class="pet-info">
                                <div class="info-row">
                                    <span class="text-text-secondary">Пол: {{ dog.gender }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="text-text-secondary">Возраст: {{ dog.age }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="text-text-secondary">Ветпаспорт: {{ dog.hasPassport ? 'есть' : 'нет' }}</span>
                                </div>
                            </div>
                            
                            <div class="pet-tags">
                                <span 
                                    v-for="tag in dog.tags" 
                                    :key="tag"
                                    class="pet-tag"
                                >
                                    {{ tag }}
                                </span>
                            </div>
                            
                            <div class="pet-buttons">
                                <button class="pet-btn-primary">
                                    ХОЧУ ЗАБРАТЬ
                                </button>
                                <button class="pet-btn-secondary">
                                    ВЗЯТЬ ПОД ОПЕКУ
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
interface Dog {
    id: number
    name: string
    gender: string
    age: string
    hasPassport: boolean
    tags: string[]
    image?: string
}

const dogs: Dog[] = [
    {
        id: 1,
        name: 'Тоби',
        gender: 'мужской',
        age: '2 года',
        hasPassport: true,
        tags: ['Дружелюбен с детьми'],
        image: '/images/pets/tobi.jpg'
    },
    {
        id: 2,
        name: 'Арчи',
        gender: 'мужской', 
        age: '4 года',
        hasPassport: true,
        tags: ['Дружелюбен с детьми', 'Любит гулять'],
        image: '/images/pets/archi.jpg'
    },
    {
        id: 3,
        name: 'Луна',
        gender: 'женский',
        age: '1 год',
        hasPassport: true,
        tags: ['Спокойная', 'Ладит с кошками']
    }
]
</script>

<style scoped>
.pet-card {
    background: linear-gradient(to top, var(--color-card-bottom-color), var(--color-card-top-color));
    border-radius: 1rem;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.pet-image {
    width: 100%;
    height: 16rem;
    background-color: #f3f4f6;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.pet-content {
    padding: 1.5rem;
}

.pet-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.info-row {
    display: flex;
    align-items: center;
}

.pet-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.pet-tag {
    border: 2px solid var(--color-accent);
    color: var(--color-accent);
    background: transparent;
    padding: 0.25rem 1rem;
    border-radius: 9999px;
    font-size: 1rem;
}

.pet-buttons {
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
}

.pet-btn-primary,
.pet-btn-secondary {
    flex: 1;
    padding: 0.5rem;
    font-size: 0.875rem;
    font-weight: bold;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Cuprum', sans-serif;
    border: none;
}

.pet-btn-primary {
    background-color: var(--color-accent);
    color: white;
}

.pet-btn-secondary {
    border: 2px solid var(--color-accent);
    color: var(--color-accent);
    background: transparent;
}

.pet-btn-secondary:hover {
    background-color: var(--color-accent);
    color: white;
}

@media (min-width: 768px) {
    .pet-btn-primary,
    .pet-btn-secondary {
        padding: 0.75rem;
        font-size: 1.25rem;
    }
}
</style>