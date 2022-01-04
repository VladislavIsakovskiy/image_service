# type: ignore[no-untyped-def]
from fastapi import APIRouter

from image_service.schemas.images import ImagesOut
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


# @router.post("/", response_model=BorrowerOut)
# async def create_item(borrower_data: BorrowerIn, session: AsyncSession = Depends(get_session)):
#     borrower = await BorrowerService(session).create_borrower(borrower_data.email)
#     return BorrowerOut.from_orm(borrower)
