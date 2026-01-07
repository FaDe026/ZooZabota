import { DogGender } from "~/types/dogGender"
declare global {
    interface News {
        id: number,
        title: string,
        date: string,
        body: string,
        author_id: number,
        tags: Tag[],
        preview: string,
        image_url: string | null,
    }

    interface Dog {
        id: number
        name: string
        age: number
        breed: string
        description: string
        intake_date: string
        veterinary_passport: boolean
        gender: DogGender

        tags: {
            id: number,
            name: string
        }[]
        image_url: string | null
    }

    interface DogSlideInfo {
        id: number
        image_url: string
    }
}

export { }