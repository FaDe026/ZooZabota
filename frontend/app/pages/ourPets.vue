<template>
    <div class="min-h-screen bg-bg font-cuprum">
        <main class="base-section pt-10">
            <div class="mx-auto base-container">
                <div class="flex justify-end mb-8">
                    <button class="font-cuprum text-text-secondary flex items-center gap-3 px-12 py-3 cursor-pointer">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M10 12.5C11.3807 12.5 12.5 11.3807 12.5 10C12.5 8.61929 11.3807 7.5 10 7.5C8.61929 7.5 7.5 8.61929 7.5 10C7.5 11.3807 8.61929 12.5 10 12.5Z"
                                stroke="#8D8D8D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                            <path
                                d="M16.1666 12.5526C16.0557 12.804 16.0226 13.0828 16.0716 13.3531C16.1207 13.6235 16.2495 13.8729 16.4416 14.0693L16.4916 14.1193C16.6466 14.2741 16.7695 14.4579 16.8534 14.6602C16.9373 14.8626 16.9805 15.0794 16.9805 15.2985C16.9805 15.5175 16.9373 15.7344 16.8534 15.9367C16.7695 16.139 16.6466 16.3228 16.4916 16.4776C16.3369 16.6326 16.153 16.7555 15.9507 16.8394C15.7484 16.9233 15.5315 16.9664 15.3125 16.9664C15.0935 16.9664 14.8766 16.9233 14.6742 16.8394C14.4719 16.7555 14.2881 16.6326 14.1333 16.4776L14.0833 16.4276C13.8869 16.2355 13.6375 16.1066 13.3671 16.0576C13.0968 16.0086 12.818 16.0417 12.5666 16.1526C12.3202 16.2583 12.11 16.4337 11.9619 16.6572C11.8138 16.8808 11.7344 17.1428 11.7333 17.411V17.5526C11.7333 17.9947 11.5577 18.4186 11.2452 18.7311C10.9326 19.0437 10.5087 19.2193 10.0666 19.2193C9.62462 19.2193 9.2007 19.0437 8.88814 18.7311C8.57558 18.4186 8.39998 17.9947 8.39998 17.5526V17.4776C8.39353 17.2018 8.30425 16.9343 8.14374 16.7099C7.98323 16.4855 7.75893 16.3145 7.49998 16.2193C7.24863 16.1084 6.96982 16.0753 6.69949 16.1243C6.42916 16.1733 6.17971 16.3022 5.98331 16.4943L5.93331 16.5443C5.77852 16.6993 5.59471 16.8222 5.39238 16.9061C5.19005 16.9899 4.97317 17.0331 4.75415 17.0331C4.53512 17.0331 4.31824 16.9899 4.11591 16.9061C3.91358 16.8222 3.72977 16.6993 3.57498 16.5443C3.42002 16.3895 3.29709 16.2057 3.21321 16.0034C3.12934 15.801 3.08617 15.5842 3.08617 15.3651C3.08617 15.1461 3.12934 14.9292 3.21321 14.7269C3.29709 14.5246 3.42002 14.3408 3.57498 14.186L3.62498 14.136C3.81709 13.9396 3.94597 13.6901 3.99498 13.4198C4.044 13.1495 4.01091 12.8706 3.89998 12.6193C3.79434 12.3728 3.61894 12.1626 3.39537 12.0146C3.17179 11.8665 2.9098 11.787 2.64165 11.786H2.49998C2.05795 11.786 1.63403 11.6104 1.32147 11.2978C1.00891 10.9852 0.833313 10.5613 0.833313 10.1193C0.833313 9.67727 1.00891 9.25335 1.32147 8.94079C1.63403 8.62823 2.05795 8.45263 2.49998 8.45263H2.57498C2.85081 8.44618 3.11832 8.3569 3.34273 8.19639C3.56714 8.03588 3.73808 7.81158 3.83331 7.55263C3.94424 7.30128 3.97733 7.02247 3.92832 6.75214C3.8793 6.48181 3.75043 6.23236 3.55831 6.03596L3.50831 5.98596C3.35335 5.83118 3.23042 5.64736 3.14655 5.44503C3.06267 5.2427 3.0195 5.02582 3.0195 4.8068C3.0195 4.58777 3.06267 4.37089 3.14655 4.16856C3.23042 3.96623 3.35335 3.78242 3.50831 3.62763C3.6631 3.47267 3.84692 3.34974 4.04925 3.26586C4.25158 3.18199 4.46845 3.13882 4.68748 3.13882C4.90651 3.13882 5.12338 3.18199 5.32571 3.26586C5.52804 3.34974 5.71186 3.47267 5.86665 3.62763L5.91665 3.67763C6.11305 3.86974 6.36249 3.99862 6.63282 4.04763C6.90315 4.09665 7.18197 4.06356 7.43331 3.95263H7.49998C7.74645 3.84699 7.95666 3.67159 8.10472 3.44802C8.25279 3.22444 8.33224 2.96245 8.33331 2.6943V2.55263C8.33331 2.1106 8.50891 1.68668 8.82147 1.37412C9.13403 1.06156 9.55795 0.885963 9.99998 0.885963C10.442 0.885963 10.8659 1.06156 11.1785 1.37412C11.4911 1.68668 11.6666 2.1106 11.6666 2.55263V2.62763C11.6677 2.89579 11.7472 3.15778 11.8952 3.38135C12.0433 3.60493 12.2535 3.78033 12.5 3.88596C12.7513 3.99689 13.0301 4.02998 13.3005 3.98097C13.5708 3.93195 13.8202 3.80308 14.0166 3.61096L14.0666 3.56096C14.2214 3.406 14.4052 3.28307 14.6076 3.1992C14.8099 3.11532 15.0268 3.07215 15.2458 3.07215C15.4648 3.07215 15.6817 3.11532 15.884 3.1992C16.0864 3.28307 16.2702 3.406 16.425 3.56096C16.5799 3.71575 16.7029 3.89957 16.7867 4.1019C16.8706 4.30423 16.9138 4.5211 16.9138 4.74013C16.9138 4.95916 16.8706 5.17603 16.7867 5.37836C16.7029 5.58069 16.5799 5.76451 16.425 5.9193L16.375 5.9693C16.1829 6.1657 16.054 6.41514 16.005 6.68547C15.956 6.9558 15.9891 7.23462 16.1 7.48596V7.55263C16.2056 7.7991 16.381 8.00931 16.6046 8.15737C16.8282 8.30544 17.0902 8.38489 17.3583 8.38596H17.5C17.942 8.38596 18.3659 8.56156 18.6785 8.87412C18.9911 9.18668 19.1666 9.6106 19.1666 10.0526C19.1666 10.4947 18.9911 10.9186 18.6785 11.2311C18.3659 11.5437 17.942 11.7193 17.5 11.7193H17.425C17.1568 11.7204 16.8948 11.7998 16.6713 11.9479C16.4477 12.0959 16.2723 12.3062 16.1666 12.5526Z"
                                stroke="#8D8D8D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <span class="text-xl">Фильтры</span>
                        <Icon name="material-symbols:keyboard-arrow-down" class="text-2xl" />
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mx-9">
                    <div v-for="dog in dogs" :key="dog.id"
                        class="bg-linear-to-b from-white to-[#F9F7F2] rounded-2xl overflow-hidden shadow-lg border border-gray-200 cursor-pointer transition-transform hover:scale-105 duration-300">
                        <NuxtLink :to="`/dog/${dog.id}`" class="block">
                            <div class="w-full h-64 bg-gray-200 flex items-center justify-center overflow-hidden">
                                <img v-if="dog.image" :src="dog.image" :alt="dog.name"
                                    class="w-full h-full object-cover">
                                <Icon v-else name="material-symbols:pets" class="text-6xl text-text-secondary" />
                            </div>

                            <div class="p-6">
                                <h3 class="section-title flex justify-center items-center">{{ dog.name }}</h3>

                                <div class="flex flex-col gap-2 mb-4">
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Пол: {{ dog.gender }}</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Возраст: {{ dog.age }}</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="text-text-secondary">Ветпаспорт: {{ dog.hasPassport ? 'есть' :
                                            'нет' }}</span>
                                    </div>
                                </div>

                                <div class="flex flex-wrap gap-2 mb-6">
                                    <span v-for="tag in dog.tags" :key="tag"
                                        class="bg-transparent border-2 border-accent text-accent text-xl font-normal rounded-full px-4 py-1">
                                        {{ tag }}
                                    </span>
                                </div>
                            </div>
                        </NuxtLink>

                        <div class="flex flex-col md:flex-row gap-2 md:gap-3 p-6 pt-0">
                            <button class="btn text-xl font-normal flex-1" @click="openTakeModal(dog)">
                                ХОЧУ ЗАБРАТЬ
                            </button>
                            <button
                                class="btn text-xl bg-transparent border-2 border-accent text-accent font-normal flex-1 hover:bg-accent hover:text-white transition-colors"
                                @click="openCustodyModal(dog)">
                                ВЗЯТЬ ПОД ОПЕКУ
                            </button>
                        </div>
                    </div>
                </div>
                <CustodyModal :is-open="isCustodyModalOpen" :dog="selectedDog" @close="closeCustodyModal"
                    @submit="handleCustodySubmit" />
                <Modal :is-open="isTakeModalOpen" title="Test" @close="closeTakeModal">
                    <div class="w-full">
                        test
                    </div>
                </Modal>
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

const isCustodyModalOpen = ref(false)
const isTakeModalOpen = ref(false)

const selectedDog = ref<Dog | undefined>(undefined)

function openTakeModal(dog: Dog) {
    isTakeModalOpen.value = true
    selectedDog.value = dog
}

function closeTakeModal ()  {
    isTakeModalOpen.value = false
    selectedDog.value = undefined
}

const openCustodyModal = (dog: Dog) => {
    selectedDog.value = dog
    isCustodyModalOpen.value = true
}

const closeCustodyModal = () => {
    isCustodyModalOpen.value = false
    selectedDog.value = undefined
}

function handleTakeSumbit(){
    closeTakeModal()
}

const handleCustodySubmit = (formData: any) => {
    console.log('Данные формы опеки:', formData)
    alert('Заявка на опеку отправлена! Мы свяжемся с вами в ближайшее время.')
    closeCustodyModal()
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