declare global {
    interface News {
        id: number,
        title: string,
        date: string,
        body: string,
        author_id: number,
        tags: string,
        preview: string,
    }
}

export { }