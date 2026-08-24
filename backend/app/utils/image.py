from io import BytesIO

from PIL import Image, UnidentifiedImageError


ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg"
}

MAX_FILE_SIZE = 5 * 1024 * 1024


def load_and_validate_image(
    image_bytes: bytes,
    content_type: str | None,
) -> Image.Image:

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "Only JPEG, PNG, JPG and WebP images are supported."
        )

    if not image_bytes:
        raise ValueError("Uploaded file is empty.")
            
        

    if len(image_bytes) > MAX_FILE_SIZE:
        raise ValueError(
            "Image size must not exceed 10 MB."
        )

    try:
        image = Image.open(
            BytesIO(image_bytes)
        )

        image.load()

    except UnidentifiedImageError as exc:
        raise ValueError(
            "Uploaded file is not a valid image."
        ) from exc

    return image.convert("RGB")