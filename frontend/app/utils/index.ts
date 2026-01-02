export const clamp = (x: number, min: number, max: number) => {
    return Math.min(Math.max(x, min), max)
}

export const ageText = (dog: Dog | undefined) => {
    if (!dog) return ""
    const lastDigit = dog.age % 10
    if (lastDigit >= 2 && lastDigit <= 4) {
        return `${dog.age} года`
    }
    if (lastDigit === 0 || (lastDigit >= 5 && lastDigit <= 9)) {
        return `${dog.age} лет`
    }
    if (lastDigit === 1) {
        return `${dog.age} год`
    }
}