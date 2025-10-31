<template>
    <div class="flex gap-4 justify-between items-stretch rounded-2xl bg-primary text-bg h-auto">
        <div class="flex items-center justify-center rounded-2xl bg-white h-40 aspect-square text-black grow z-10 ">
            <Icon name="mage:user" class="h-[70%] w-full"></Icon>
        </div>
        <div class=" flex flex-col justify-between py-2">
            <div class="flex flex-col ">
                <h2 class="text-2xl">Фамилия имя</h2>
                <span class="text-secondary">Директор приюта</span>
            </div>
            <div class="flex flex-col">
                <span>+7(800)-555-35-35</span>
                <span>1234@mail.ru</span>
            </div>
        </div>
        <div class="flex flex-col justify-end py-2 pr-2">
            <div class="flex gap-1">
                <span class="flex justify-center items-center bg-[#0077ff] p-2.5 rounded-full">
                    <svg width="20" height="20" viewBox="0 0 22 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M11.9825 13.6038C4.46596 13.6038 0.178638 8.49727 0 0H3.76515C3.88882 6.23678 6.66459 8.87856 8.86321 9.42326V0H12.4085V5.37888C14.5796 5.14739 16.8607 2.69625 17.6302 0H21.1755C20.8855 1.39835 20.3075 2.72237 19.4776 3.88923C18.6477 5.0561 17.5837 6.04071 16.3523 6.78148C17.7269 7.45834 18.941 8.41638 19.9145 9.59238C20.888 10.7684 21.5988 12.1356 22 13.6038H18.0974C17.7373 12.3286 17.0054 11.187 15.9934 10.3222C14.9814 9.45741 13.7343 8.90785 12.4085 8.74239V13.6038H11.9825Z"
                            fill="white" />
                    </svg>
                </span>
                <span class="flex justify-center items-center bg-[#27a6e5] p-2.5 rounded-full">
                    <svg width="19" height="20" viewBox="0 0 19 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M19 0.585183L15.9946 15.8312C15.9946 15.8312 15.5741 16.8883 14.4189 16.3813L7.48458 11.0313L7.45242 11.0155C8.38909 10.1692 15.6524 3.59788 15.9698 3.30001C16.4613 2.83869 16.1562 2.56405 15.5856 2.91254L4.85679 9.76848L0.717638 8.36709C0.717638 8.36709 0.0662573 8.13394 0.00359284 7.62698C-0.0598962 7.11919 0.739076 6.84456 0.739076 6.84456L17.6131 0.1836C17.6131 0.1836 19 -0.42956 19 0.585183Z"
                            fill="#FEFEFE" />
                    </svg>
                </span>
            </div>
        </div>
    </div>
</template>