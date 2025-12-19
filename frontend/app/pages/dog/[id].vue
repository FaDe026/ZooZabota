<template>
    <div class="min-h-screen bg-bg font-cuprum">
        <main class="base-section pt-10">
            <div class="mx-auto base-container">
                <div class="mb-8">
                    <NuxtLink to="/ourPets" class="text-text-secondary text-xl hover:text-primary transition-colors">
                        ← Назад к питомцам
                    </NuxtLink>
                </div>
                <div v-if="dog" class="flex justify-center">
                    <div class="bg-linear-to-b from-white to-[#F9F7F2] rounded-2xl overflow-hidden shadow-lg border border-gray-200 w-full max-w-2xl mx-9">
                        <div class="w-full h-96 bg-gray-200 flex items-center justify-center overflow-hidden">
                            <img 
                                v-if="dog.image" 
                                :src="dog.image" 
                                :alt="dog.name" 
                                class="w-full h-full object-cover"
                            >
                            <Icon 
                                v-else 
                                name="material-symbols:pets" 
                                class="text-6xl text-text-secondary" />
                        </div>
                        
                        <div class="p-6">
                            <h3 class="section-title flex justify-center items-center mb-4">{{ dog.name }}</h3>
                            <div class="mb-6">
                                <p class="text-xl text-text-primary leading-relaxed">
                                    {{ dog.description }}
                                </p>
                            </div>
                            <div class="flex flex-col gap-2 mb-4">
                                <div class="flex items-center">
                                    <span class="text-text-secondary">Пол: {{ dog.gender }}</span>
                                </div>
                                <div class="flex items-center">
                                    <span class="text-text-secondary">Возраст: {{ dog.age }}</span>
                                </div>
                                <div class="flex items-center">
                                    <span class="text-text-secondary">Ветпаспорт: {{ dog.hasPassport ? 'есть' : 'нет' }}</span>
                                </div>
                            </div>
                            
                            <div class="flex flex-wrap gap-2 mb-6">
                                <span 
                                    v-for="tag in dog.tags" 
                                    :key="tag"
                                    class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1">
                                    {{ tag }}
                                </span>
                            </div>
                            
                            <div class="flex flex-col md:flex-row gap-2 md:gap-3">
                                <button class="btn text-xl font-normal flex-1">
                                    ХОЧУ ЗАБРАТЬ
                                </button>
                                <button 
                                    @click="openCustodyModal"
                                    class="btn text-xl bg-transparent border-2 border-accent text-accent font-normal flex-1 hover:bg-accent hover:text-white transition-colors">
                                    ВЗЯТЬ ПОД ОПЕКУ
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="text-center py-20">
                    <p class="text-2xl text-text-secondary">Собака не найдена</p>
                    <NuxtLink to="/ourPets" class="btn mt-4 inline-block">
                        Вернуться к питомцам
                    </NuxtLink>
                </div>
                <CustodyModal 
                    :is-open="isCustodyModalOpen" 
                    :dog="dog"
                    @close="closeCustodyModal"
                    @submit="handleCustodySubmit"/>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import CustodyModal from '~/components/CustodyModal.vue'

definePageMeta({
    layout: 'default'
})

const route = useRoute()
const dogId = parseInt(route.params.id as string)

const isCustodyModalOpen = ref(false)

const openCustodyModal = () => {
    console.log('Opening custody modal') 
    isCustodyModalOpen.value = true
}

const closeCustodyModal = () => {
    console.log('Closing custody modal') 
    isCustodyModalOpen.value = false
}

const handleCustodySubmit = (formData: any) => {
    console.log('Данные формы опеки:', formData)
    alert('Заявка на опеку отправлена! Мы свяжемся с вами в ближайшее время.')
}

interface Dog {
    id: number
    name: string
    gender: string
    age: string
    hasPassport: boolean
    size: string
    description: string
    history: string
    character: string
    tags: string[]
    image?: string
    extraImages?: string[]
}

const dogsDatabase: Dog[] = [
    {
        id: 1,
        name: 'Тоби',
        gender: 'мужской',
        age: '2 года',
        hasPassport: true,
        size: 'Средний',
        description: 'Тоби — зрелый, спокойный и уравновешенный пёс с внимательными и умным взглядом. Жизненные испытания подарили ему мудрость, но не отняли надежду. Он не навязчив, ценит спокойную атмосферу и проявляет удивительную чуткость к настроению человека. Тоби идеально подойдет для семьи или человека, ищущего преданного и несучтившего друга.',
        history: 'Тоби знал, что такое дом и любящая семья, но волею обстоятельств оказался на улице. Пройдя через трудности, он был подобран волонтёрами и поменял в приюте. Здесь он залечил не только физические, но и душевные раны, заново научившись доверять людям. Его прошлый опыт сделал его особенно ценящим заботу и надёжность.',
        character: 'Спокойный, уравновешенный, преданный, чуткий к настроению человека',
        tags: ['Дружелюбен с детьми', 'Спокойный', 'Для семьи', 'Опыт в доме'],
        image: '/images/pets/tobi.jpg'
    },
    {
        id: 2,
        name: 'Арчи',
        gender: 'мужской',
        age: '4 года',
        hasPassport: true,
        size: 'Крупный',
        description: 'Арчи — энергичный и жизнерадостный пёс, который обожает активные прогулки и игры. Он очень общительный и быстро находит общий язык как с людьми, так и с другими собаками.',
        history: 'Арчи попал в приют после того, как его предыдущие хозяева переехали в другой город и не смогли взять его с собой. Несмотря на грустное прошлое, он сохранил оптимизм и веру в людей.',
        character: 'Энергичный, дружелюбный, игривый, легко обучаемый',
        tags: ['Энергичный', 'Дружелюбный', 'Для активных людей', 'Любит гулять'],
        image: '/images/pets/archi.jpg'
    },
    {
        id: 3,
        name: 'Луна',
        gender: 'женский',
        age: '1 год',
        hasPassport: true,
        size: 'Мелкий',
        description: 'Луна — нежная и ласковая собачка, которая станет прекрасным компаньоном. Она очень привязчива и обожает проводить время рядом с хозяином.',
        history: 'Луну нашли на улице совсем щенком. Она прошла долгий путь реабилитации и теперь готова к переезду в любящую семью.',
        character: 'Спокойная, ласковая, послушная, немного робкая вначале',
        tags: ['Спокойная', 'Ладит с кошками', 'Для квартиры', 'Ласковая'],
        image: '/images/pets/luna.jpg'
    }
]

const dog = dogsDatabase.find(dog => dog.id === dogId)
if (!dog) {
    throw createError({
        statusCode: 404,
        statusMessage: 'Собака не найдена'
    })
}
</script>