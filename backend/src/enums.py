from enum import Enum


class GenderEnum(Enum):
    MALE = 'M'
    FEMALE = 'F'


class RequestStatusEnum(Enum):
    NEW = 'Новая'
    IN_PROGRESS = 'В работе'
    COMPLETED = 'Завершена'


class FamilyMemberCountEnum(Enum):
    ONE = "Я один/одна"
    WITH_CHILDREN = "Семья с детьми"
    COUPLE = "Пара"


class PetExperienceEnum(Enum):
    FIRST_PET = "Это будет первый питомец"
    HAD_PETS_BEFORE = "Ранее были кошки/собаки"
    CURRENTLY_HAVE_PETS = "На данный момент имеются животные в семье"


class AdoptionPurposeEnum(Enum):
    FOR_SELF = "Для себя"
    AS_GIFT = "В подарок"


class HousingTypeEnum(Enum):
    RENTED = "Арендую жилье"
    APARTMENT = "Квартира"
    HOUSE = "Частный дом"


class HousingAreaEnum(Enum):
    UP_TO_40 = "До 40 м2"
    BETWEEN_40_60 = "40–60 м2"
    OVER_60 = "Более 60 м2"

class RequestTypeEnum(Enum):
    ADOPTION_REQUEST = "Усыновление"
    GUARDIAN_REQUEST = "Опека"