export const apiFetch = async <T = any>(
  url: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    headers?: HeadersInit
    body?: BodyInit | null
    [key: string]: any
  } = {}
) => {
  const token = localStorage.getItem('access_token')
  const baseURL = 'http://localhost:8000'

  const headers = new Headers(options.headers)
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  return $fetch<T>(`${baseURL}${url}`, {
    ...options,
    method: options.method?.toUpperCase() as any,
    headers
  })
}