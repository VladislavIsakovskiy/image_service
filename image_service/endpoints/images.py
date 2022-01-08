# type: ignore[no-untyped-def]
from fastapi import APIRouter, File, UploadFile

from image_service.schemas.images import ImageInfo, ImageStatusOut, ImagesOut
from image_service.services.image import ImageService

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ImagesOut)
async def read_images():
    images = await ImageService().get_images_info()
    return ImagesOut(images=images)


@router.get("/{image_name}/", response_model=ImageInfo)
async def read_image(image_name: str):
    image_info = await ImageService().get_image_info(image_name)
    return image_info


@router.get("/{image_name}/delete", response_model=ImageStatusOut)
async def delete_image(image_name: str):
    deleted_image_status_message = await ImageService().delete_image(image_name)
    return ImageStatusOut(message=deleted_image_status_message)


@router.post("/upload_image", response_model=ImageStatusOut)
async def upload_image(name: str, image_file: UploadFile = File(None)):
    added_image_status = await ImageService().add_image_from_file(name, image_file)
    return ImageStatusOut(message=added_image_status)


@router.post("/upload_image_from_bytes", response_model=ImageStatusOut)
async def upload_image_from_bytes(name: str, image_bytes: str):
    added_image_status = await ImageService().add_image_from_bytes(name, image_bytes)
    return ImageStatusOut(message=added_image_status)
