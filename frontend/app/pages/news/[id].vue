<script lang="ts" setup>
const router = useRouter()

function backClicked() {
    router.back()
}

</script>
<template>
    <section class="base-section">
        <div class="base-container mx-auto relative flex justify-center items-center mb-7">
            <svg class="absolute left-0 cursor-pointer" @click="backClicked()" width="55" height="47"
                viewBox="0 0 55 47" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M43.5416 23.5H11.4583" stroke="#1A3C40" stroke-width="5" stroke-linecap="round"
                    stroke-linejoin="round" />
                <path d="M27.4999 37.2083L11.4583 23.5L27.4999 9.79166" stroke="#1A3C40" stroke-width="5"
                    stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <h1 class="text-2xl text-primary text-center font-bold">Пропала собака</h1>
        </div>
        <div class="base-container flex flex-col mx-auto">
            <img class="w-full aspect-video object-cover rounded-xl shadow-xl/10 self-center" src="/images/news/1.png"
                alt="">
            <div class="text-text-primary text-lg">
                Пропала собака! Заволжский район
                Друзья, жители района «Зеленый Бор» и все неравнодушные! Наша семья в отчаянии: 15 октября, во вторник
                днем, пропала наша любимая собака по кличке Буся.
                <br>
                <br>
                Буся — девочка, палевого окраса, 3 года. Пропала в районе Центрального парка, недалеко от детской
                площадки. Очень добрая, общительная и совершенно неагрессивная.
                <br> 
                <br> 
                ОСОБЫЕ ПРИМЕТЫ:
                <br>  
                На левом ухе небольшой светлый шрам (с детства).
                <br>
                <br>
                Мы очень по ней скучаем. Для наших детей — это член семьи. Любая информация может быть решающей!
                <br>
                <br>
                Если вы видели Бусю, брали ее к себе или знаете, где она может находиться, позвоните в любое время:
                <br>
                <br>
                +7 (XXX) XXX-XX-XX (Анна)
            </div>
        </div>
    </section>
</template>