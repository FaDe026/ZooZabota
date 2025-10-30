<template>
    <section class="flex justify-center pt-20 py-15 px-2">
        <div
            class="relative flex flex-col items-center gap-6 w-full max-w-7xl bg-primary text-bg text-lg px-8 py-10 rounded-2xl mt-55">
            <img class="absolute top-[-210px] left-1/2 translate-x-[-50%] object-cover h-auto w-60"
                src="/images/dog.png" alt="собака">
            <p class="text-xl w-full">
                Наш приют — это временный дом для тех, кто его лишился. Здесь каждый хвостик ждёт своего Человека,
                готовый подарить всю свою любовь и преданность. Каждый день мы работаем, чтобы изменить судьбу брошенных
                животных. Наша команда — это ветеринары, волонтеры и просто неравнодушные люди. Вместе мы лечим,
                социализируем и ищем любящие руки для наших подопечных. Но наша миссия невыполнима без вашей поддержки.
            </p>
            <h2 class="text-3xl text-alert">Ваша помощь превращает историю потери в историю спасения!</h2>
            <button class="btn">Выбрать питомца</button>
        </div>
    </section>

    <section class="flex justify-center py-15 px-2">
        <div class="flex flex-col items-center w-full max-w-7xl gap-10">
            <h2 class="section-title">Наши питомцы</h2>
            <div
                class="w-full h-[460px] flex justify-center items-center text-primary text-2xl border border-primary rounded-2xl">
                Здесь будет крутой 3д слайдер
            </div>
            <button class="btn">Посмотреть всех</button>
        </div>
    </section>

    <section class="flex justify-center py-15 px-2">
        <div class="flex flex-col items-center w-full max-w-7xl gap-10">
            <h2 class="section-title">Как помочь нашему приюту</h2>
            <div class="flex flex-col border-t border-b border-primary w-full ">
                <a class="border-b border-primary text-2xl text-primary p-2 w-full flex items-center justify-between last:border-0"
                    href="">
                    <span>Самостоятельно привезти корм</span>
                    <Icon name="material-symbols:arrow-right-alt"></Icon>
                </a>
                <a class="border-b border-primary text-2xl text-primary p-2 w-full flex items-center justify-between last:border-0"
                    href="">
                    <span>Отправить корм через OZON</span>
                    <Icon name="material-symbols:arrow-right-alt"></Icon>
                </a>
                <a class="border-b border-primary text-2xl text-primary p-2 w-full flex items-center justify-between last:border-0"
                    href="">
                    <span>Принести ненужные пледы, одеяла</span>
                    <Icon name="material-symbols:arrow-right-alt"></Icon>
                </a>
                <a class="border-b border-primary text-2xl text-primary p-2 w-full flex items-center justify-between last:border-0"
                    href="">
                    <span>Сделать перевод на карту</span>
                    <Icon name="material-symbols:arrow-right-alt"></Icon>
                </a>
                <a class="border-b border-primary text-2xl text-primary p-2 w-full flex items-center justify-between last:border-0"
                    href="">
                    <span>Помочь с выгулом собак</span>
                    <Icon name="material-symbols:arrow-right-alt"></Icon>
                </a>
            </div>
        </div>
    </section>

    <section class="flex justify-center py-15 px-2">
        <div class="max-w-7xl">
            <h2 class="section-title">Последние новости</h2>
        </div>
    </section>


    <section class="flex justify-center py-15 px-2">
        <div class="max-w-7xl">
            <h2 class="section-title">Контакты</h2>
            <div>
                <!-- Карточка -->
                <div class="flex gap-2 justify-between items-stretch rounded-2xl bg-primary h-auto">
                    <div class="rounded-2xl bg-white w-30 grow z-10"></div>
                    <div>
                        <h2>Фамилия имя</h2>
                        <span>Директор приюта</span>
                        
                    </div>
                    <div></div>
                </div>

            </div>
        </div>
    </section>
</template>