from fastapi import HTTPException

def parse_tag_ids(tag_ids_str: str | None) -> list[int]:
    if not tag_ids_str:
        return []
    try:
        return [int(x.strip()) for x in tag_ids_str.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Неверный формат tag_ids. Ожидаются целые числа, разделённые запятыми (например: 1,2,3)."
        )