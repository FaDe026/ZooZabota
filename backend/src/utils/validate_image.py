import uuid
from pathlib import Path as SysPath
from fastapi import HTTPException, UploadFile

UPLOAD_DIR = SysPath("static/dogs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def validate_and_save_dog_image(file: UploadFile) -> str:
    image_url = None
    if file:
        if file.content_type not in ("image/jpeg", "image/png", "image/jpg"):
            raise HTTPException(400, "Разрешены только JPEG и PNG изображения")

        ext = file.filename.split(".")[-1].lower() if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        image_url = f"/static/dogs/{filename}"
    return image_url

NEWS_UPLOAD_DIR = SysPath("static/news")
NEWS_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def validate_and_save_news_image(file: UploadFile) -> str | None:
    """Валидирует и сохраняет изображение для новости. Возвращает URL или None."""
    if not file:
        return None

    if file.content_type not in ("image/jpeg", "image/png", "image/jpg"):
        raise HTTPException(400, "Разрешены только JPEG и PNG изображения")

    ext = file.filename.split(".")[-1].lower() if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = NEWS_UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return f"/static/news/{filename}"
