import { apiFetch } from '~/composables/useAPI'

export const useTags = <T = any>() => {
  return useAsyncData<T>('tags', () => apiFetch('/tags'))
}