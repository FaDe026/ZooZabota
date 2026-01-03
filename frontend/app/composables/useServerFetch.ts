import type { UseFetchOptions } from 'nuxt/app';
import { useNuxtApp } from '#app';

export default function <T>(url: string, options: UseFetchOptions<T> = {}) {
    const { $serverFetch } = useNuxtApp();

    return useFetch(url, {
        ...options,
        $fetch: $serverFetch as typeof $fetch, // Use your custom fetch instance
    });
}
