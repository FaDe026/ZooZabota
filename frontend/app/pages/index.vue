<template>
    <section class="base-section pt-20">
        <div
            class="mx-auto relative flex flex-col items-center gap-6 w-full max-w-7xl card-bg card-shadow text-bg text-lg px-8 py-10 rounded-2xl mt-55">
            <img class="absolute top-[-210px] left-1/2 translate-x-[-50%] object-cover h-auto w-60"
                src="/images/dog.png" alt="собака">
            <p class="text-xl text-text-primary w-full ">
                Наш приют — это временный дом для тех, кто его лишился. Здесь каждый хвостик ждёт своего Человека,
                готовый подарить всю свою любовь и преданность. Каждый день мы работаем, чтобы изменить судьбу брошенных
                животных. Наша команда — это ветеринары, волонтеры и просто неравнодушные люди. Вместе мы лечим,
                социализируем и ищем любящие руки для наших подопечных. Но наша миссия невыполнима без вашей поддержки.
            </p>
            <h2 class="text-3xl text-primary">Ваша помощь превращает историю потери в историю спасения!</h2>
            <button class="btn uppercase">Помочь приюту</button>
        </div>
    </section>

    <section class="base-section">
        <div class="mx-auto flex flex-col items-center base-container gap-10 justify-center">
            <h2 class="section-title ">За время работы приюта</h2>
            <div class="flex flex-col justify-center gap-5 w-full">
                <div class="base-card text-3xl w-full text-center">
                    более <span class="font-bold">15</span> лет дарим надежду
                </div>
                <div class="base-card text-3xl w-full text-center">
                    <span class="font-bold">377+</span> питомцев нашли свой дом
                </div>
                <div class="base-card text-3xl w-full text-center">
                    <span class="font-bold">10+</span> волонтеров в нашей команде
                </div>
            </div>
        </div>
    </section>

    <section class="base-section">
        <div class="mx-auto flex flex-col items-center base-container gap-10">
            <h2 class="section-title">Наши питомцы</h2>
            <div
                class="w-full h-[460px] flex justify-center items-center text-primary text-2xl border border-primary rounded-2xl">
                Здесь будет крутой 3д слайдер
            </div>
            <button class="btn">Выбрать питомца</button>
        </div>
    </section>

    <section class="base-section">
        <div class="mx-auto flex flex-col items-center w-full max-w-7xl gap-10">
            <h2 class="section-title">Как помочь нашему приюту</h2>
            <div class="flex flex-col gap-5 w-full">
                <a class="base-card index-card-link" href="">
                    <span>Самостоятельно привезти корм</span>
                </a>
                <a class="base-card index-card-link" href="">
                    <span>Отправить корм через OZON</span>
                </a>
                <a class="base-card index-card-link" href="">
                    <span>Принести ненужные пледы, одеяла</span>
                </a>
                <a class="base-card index-card-link" href="">
                    <span>Сделать перевод на карту</span>
                </a>
                <a class="base-card index-card-link" href="">
                    <span>Помочь с выгулом собак</span>
                </a>
            </div>
        </div>
    </section>

    <section class="base-section">
        <div class="mx-auto flex flex-col items-center max-w-7xl w-full gap-10">
            <h2 class="section-title">Последние новости</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 w-full gap-5">
                <IndexNewsCard img-src="/images/news/1.png" title="Пропала собака! Заволжский район"></IndexNewsCard>
                <IndexNewsCard img-src="/images/news/2.png" title="У нас прошла вакцинация"></IndexNewsCard>
                <IndexNewsCard img-src="/images/news/3.png"
                    title="Красавец Лакки нашёл своих хозяев и отправился домой!"></IndexNewsCard>
            </div>
        </div>
    </section>


    <section class="base-section">
        <div class="mx-auto flex flex-col items-center max-w-7xl w-full gap-10">
            <h2 class="section-title text-center ">Контакты</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 auto-rows-max w-full gap-5">
                    <IndexContactCard></IndexContactCard>
                    <IndexContactCard></IndexContactCard>
                    <IndexContactCard></IndexContactCard>
                    <IndexContactCard></IndexContactCard>
                    <IndexContactCard></IndexContactCard>
                    <IndexContactCard></IndexContactCard>
            </div>
        </div>
    </section>
</template>