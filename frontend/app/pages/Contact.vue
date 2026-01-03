<template>
  <section class="base-section flex justify-center">
    <div class="base-container flex flex-col items-start gap-6 w-full">
      <h1 class="text-2xl font-semibold text-text-primary text-center w-full">Контакты</h1>

      <div class="w-full flex flex-col items-start gap-3">
        <span class="text-xl text-text-primary">
          Позвонить:
        </span>

        <a href="tel:88005553535" class="w-full flex justify-center items-center rounded-xl bg-accent text-white text-2xl py-4">
          8&nbsp;(800)&nbsp;555&nbsp;35&nbsp;35
        </a>
      </div>
      
      <div class="flex flex-col gap-1 text-text-secondary text-lg text-left w-full">
        <span>Email: 123@mail.ru</span>
        <span>Адрес: г. Москва, ул. Октябрьская, д.3 стр. 2</span>
      </div>
      <div class="flex flex-col items-start gap-3 pt-4 w-full">
        <span class="text-xl text-text-primary">
          Мы в социальных сетях
        </span>

        <div class="flex gap-3">
          <a href="#" class="flex justify-center items-center bg-[#0077ff] p-2.5 rounded-full hover:opacity-90 transition-opacity">
            <svg width="20" height="20" viewBox="0 0 22 14" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M11.9825 13.6038C4.46596 13.6038 0.178638 8.49727 0 0H3.76515C3.88882 6.23678 6.66459 8.87856 8.86321 9.42326V0H12.4085V5.37888C14.5796 5.14739 16.8607 2.69625 17.6302 0H21.1755C20.8855 1.39835 20.3075 2.72237 19.4776 3.88923C18.6477 5.0561 17.5837 6.04071 16.3523 6.78148C17.7269 7.45834 18.941 8.41638 19.9145 9.59238C20.888 10.7684 21.5988 12.1356 22 13.6038H18.0974C17.7373 12.3286 17.0054 11.187 15.9934 10.3222C14.9814 9.45741 13.7343 8.90785 12.4085 8.74239V13.6038H11.9825Z"
                fill="white"
              />
            </svg>
          </a>
          <a href="#" class="flex justify-center items-center bg-[#27a6e5] p-2.5 rounded-full hover:opacity-90 transition-opacity">
            <svg width="19" height="20" viewBox="0 0 19 17" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M19 0.585183L15.9946 15.8312C15.9946 15.8312 15.5741 16.8883 14.4189 16.3813L7.48458 11.0313L7.45242 11.0155C8.38909 10.1692 15.6524 3.59788 15.9698 3.30001C16.4613 2.83869 16.1562 2.56405 15.5856 2.91254L4.85679 9.76848L0.717638 8.36709C0.717638 8.36709 0.0662573 8.13394 0.00359284 7.62698C-0.0598962 7.11919 0.739076 6.84456 0.739076 6.84456L17.6131 0.1836C17.6131 0.1836 19 -0.42956 19 0.585183Z"
                fill="#FEFEFE"
              />
            </svg>
          </a>
          <a href="#" class="flex justify-center items-center bg-[#48c95f] p-2.5 rounded-full hover:opacity-90 transition-opacity">
            <svg width="21" height="21" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M17.9268 3.0625C15.9512 1.09375 13.3171 0 10.5366 0C4.7561 0 0.0731696 4.66667 0.0731696 10.4271C0.0731696 12.25 0.585366 14.0729 1.46341 15.6042L0 21L5.56098 19.5417C7.09756 20.3438 8.78049 20.7812 10.5366 20.7812C16.3171 20.7812 21 16.1146 21 10.3542C20.9268 7.65625 19.9024 5.03125 17.9268 3.0625Z"
                fill="white"
              />
            </svg>
          </a>
        </div>
      </div>

      <div class="w-full flex flex-col items-start gap-3">
        <span class="text-xl text-text-primary">
          Реквизиты
        </span>
        <div class="flex flex-col gap-1 text-text-secondary text-lg text-left w-full">
        <span>Номер карты Сбербанк России: 5469770013930269 Держатель карты Оксана Сергеевна Н.</span>
        <span>"Голодный" телефон: 9066371153</span>
        <span>Киви-кошелек: 9066371153</span>
        <span>Яндекс Кошелек: 41001401541495</span>
      </div>
      </div>
      <h2 class="text-xl text-text-primary text-center w-full">Руководство</h2>
      <div class="mx-auto flex flex-col items-center max-w-7xl w-full gap-10">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 auto-rows-max w-full gap-5 px-4 sm:px-6 lg:px-8">
              <ContactCard></ContactCard>
              <ContactCard></ContactCard>
              <ContactCard></ContactCard>
              <ContactCard></ContactCard>
              <ContactCard></ContactCard>
              <ContactCard></ContactCard>
          </div>
      </div>
    </div>
  </section>
</template>