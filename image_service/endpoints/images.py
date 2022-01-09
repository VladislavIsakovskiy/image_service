# type: ignore[no-untyped-def]
from fastapi import APIRouter

from image_service.schemas.images import ImageIn, ImageInfo, ImagesOut
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


@router.delete("/{image_name}/delete", response_model=str)
async def delete_image(image_name: str):
    deleted_image_status_message = await ImageService().delete_image(image_name)
    return deleted_image_status_message


@router.post("/upload_image", response_model=str)
async def upload_image(image_data: ImageIn):
    added_image_status = await ImageService().add_image(image_data.name, image_data.image_str)
    return added_image_status
