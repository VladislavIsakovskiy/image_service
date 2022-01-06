# type: ignore[no-untyped-def]
from fastapi import APIRouter

from image_service.schemas.images import Image, ImageDeleteOut, ImagesOut
from image_service.services.image import ImageService

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ImagesOut)
async def read_images():
    images = ImageService().get_images()
    return ImagesOut(images=images)


@router.get("/{image_name}/", response_model=Image)
async def read_image(image_name: str):
    image_info = ImageService().get_image_info(image_name)
    return image_info


@router.get("/{image_name}/delete", response_model=ImageDeleteOut)
async def delete_image(image_name: str):
    status_message = ImageService().delete_image(image_name)
    return ImageDeleteOut(message=status_message)
