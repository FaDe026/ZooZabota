import { ofetch } from 'ofetch';

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig();

    const serverFetch = ofetch.create({
        baseURL: config.public.apiBase,
    });

    return {
        provide: {
            serverFetch
        },
    };
})