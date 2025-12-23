import { DogGender } from "~/types/dogGender"
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

    interface Dog {
        id: number
        name: string
        age: number
        breed: string
        description: string
        intake_date: string
        vetirinary_passport: boolean
        gender: DogGender

        tags: string[]
        image?: string
    }
}

export { }