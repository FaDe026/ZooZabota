export default function () {
    const config = useRuntimeConfig()

    return useFetch<News[]>("/news", {
        baseURL: config.public.apiBase
    })
}