<template>
    <section class="flex flex-col items-center gap-4 px-2 py-4">
        <h1 class="text-text-primary text-2xl text-center">Помочь приюту можно здесь</h1>
        <h2 class="text-accent text-xl text-center">Ваша помощь спасает жизни<br>Каждый рубль важен для наших подопечных
        </h2>
        <div class="max-w-3xl w-full flex flex-col gap-4 p-3 card-bg shadow-xl rounded-md">
            <h2 class="text-text-primary text-center text-xl">Сделать пожертвование</h2>
            <div>
                <LabeledRadio name="donationType">
                    Разовое пожертвование
                </LabeledRadio>
                <LabeledRadio name="donationType">
                    Регулярное пожертвование
                </LabeledRadio>
            </div>
            <div>
                <LabeledRadio name="donationAmount">
                    100
                </LabeledRadio>
                <LabeledRadio name="donationAmount">
                    500
                </LabeledRadio>
                <LabeledRadio name="donationAmount">
                    1000
                </LabeledRadio>
                <LabeledRadio name="donationAmount" class="">
                    <span>Ваша сумма</span>
                    <input type="text" class="outline-0 border-b border-input-border">
                </LabeledRadio>
            </div>
            <div>
                <LabeledCheckbox name="offerAgreement">
                    Соглашаюсь с офертой
                </LabeledCheckbox>
                <LabeledCheckbox name="personalDataConsent">
                    Соглашаюсь на обработку персональных данных
                </LabeledCheckbox>
            </div>
            <button class="btn self-center px-6 py-1">Пожертвовать</button>
        </div>
        <h1 class="text-text-primary text-2xl text-center">Актуальный список вещей для пожертвований</h1>
        <div class="flex flex-col gap-3 max-w-6xl">
            <p>
                Нам нужны:
            </p>
            <ul class="pl-10 list-disc">
                <li>пледы</li>
                <li>шерстяные одеяла</li>
                <li>старое, но чистое постельное белье</li>
            </ul>
            <p class="text-text-primary">
                Однако, пожалуйста, помните, что приют не принимает одеяла, подушки с наполнителями, так как животные
                могут их повредить.
                Важно поддерживать приют чистым и безопасным для всех его обитателей.
            </p>
            <p class="text-text-primary">
                Передать можно по адресу: ХХХ<br>Предварительно, связавшись с работниками приюта<br>Иванов Иван - 8(800)
                555-35-35
            </p>
        </div>
        <h1 class="text-text-primary text-2xl text-center">Мы с радостью принимаем гостей<br>Групповые посещения
            приветствуются!</br></h1>
        <div class="max-w-3xl w-full flex flex-col gap-4 p-3 card-bg shadow-xl rounded-md">
            <h2 class="text-text-primary text-center text-xl">Запись на групповое посещение</h2>
            <form action="" class="flex flex-col gap-2">
                <div>
                    <label for="name" class="text-text-secondary">Фамилия имя</label>
                    <TextInput input-id="name" placeholder="Иван Иванов" class="mb-2"></TextInput>
                </div>
                <div>
                    <label for="phoneInput" class="text-text-secondary">Телефон</label>
                    <TextInput input-id="phoneInput" placeholder="+7 (800) 55-35-34" class="mb-2"></TextInput>
                </div>
                <div>
                    <label class="text-text-secondary">Количество человек</label>
                    <InputNumber></InputNumber>
                </div>
            </form>
            <button class="btn self-center px-6 py-1">Записаться</button>
        </div>

    </section>
</template>