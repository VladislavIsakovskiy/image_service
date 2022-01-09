import base64
import glob
import io
import ntpath
import os
from typing import List

from PIL import Image, UnidentifiedImageError

from dotenv import load_dotenv

from fastapi import File

from image_service.errors import APIImageAlreadyExists, APIImageMaxSizeExceeded, \
    APIImageNotDeleted, APIImageNotFound, APIImageWrongFormat
from image_service.schemas.images import ImageInfo

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join(CURRENT_DIR, "..", "..", "images")


class ImageService:
    async def get_images_info(self) -> list[ImageInfo]:
        """
        Returns info for all images that contain server (images folder)
        :return: list[ImageInfo]
        """
        images = []
        relevant_extensions = ("*.png", "*.jpg")
        image_paths = await self._get_all_relevant_image_paths(relevant_extensions)
        for image_path in image_paths:
            image = await self._generate_image_info(image_path)
            images.append(image)
        return images

    async def get_image_info(self, image_name: str) -> ImageInfo:
        """
        Returns info for particular image using it's name as input parameter
        If image with some name not exists raise APIImageNotFound exception
        :param image_name: str
        :return: ImageInfo
        """
        image_path = await self._get_image_path(image_name)
        is_image_exists = await self._check_if_image_exists(image_path)
        if is_image_exists is False:
            raise APIImageNotFound(image_name)
        return await self._generate_image_info(image_path)

    async def delete_image(self, image_name: str) -> str:
        """
        Delete particular image and return message in case of success using it's name as input parameter
        If image with some name not exists raise APIImageNotFound exception
        If existed image didn't deleted raise APIImageNotDeleted exception
        :param image_name:  str
        :return: str
        """
        image_path = await self._get_image_path(image_name)
        is_image_exists = await self._check_if_image_exists(image_path)
        if is_image_exists is False:
            raise APIImageNotFound(image_name)
        os.remove(image_path)
        is_image_exists = await self._check_if_image_exists(image_path)
        if is_image_exists is True:
            raise APIImageNotDeleted(image_name)
        return f"Image {image_name} deleted successfully!"

    async def add_image(self, image_name: str, image_str: str) -> str:
        """
        Add new image to server and return message in case of success
        If image with similar name already exists raise APIImageAlreadyExists exception
        If there are some problems with opening or format with image file raise APIImageWrongFormat exception
        If image file's size more than max_size from .env raise APIImageMaxSizeExceeded exception
        :param image_name: str
        :param image_str: str
        :return: str
        """
        image_path = await self._get_image_path(image_name)
        is_image_exists = await self._check_if_image_exists(image_path)
        if is_image_exists is True:
            raise APIImageAlreadyExists(image_name)
        decoded_image_str = base64.b64decode(image_str)
        await self._check_image(io.BytesIO(decoded_image_str))
        new_image = Image.open(io.BytesIO(decoded_image_str))
        new_image.save(image_path)
        return f"Image {image_name} uploaded successfully!"

    @staticmethod
    async def _get_image_path(image_name: str) -> str:
        image_path = os.path.join(IMAGES_FOLDER, image_name)
        return image_path

    @staticmethod
    async def _check_if_image_exists(image_path: str) -> bool:
        return os.path.exists(image_path)

    @staticmethod
    async def _get_all_relevant_image_paths(relevant_extensions: tuple) -> List[str]:
        image_paths = []
        for ext in relevant_extensions:
            image_paths.extend(glob.glob(os.path.join(IMAGES_FOLDER, ext)))
        return image_paths

    @staticmethod
    async def _generate_image_info(image_path: str) -> ImageInfo:
        """
        Return ImageInfo object using path of image as input parameter
        :param image_path: str
        :return: ImageInfo
        """
        image_name = ntpath.basename(image_path)
        byte_size = os.stat(image_path).st_size
        mb_size = round(byte_size / (1024 * 1024), 2)
        str_size = f"{mb_size} MB"
        changed = os.path.getmtime(image_path)
        image = ImageInfo(name=image_name, size=str_size, last_change_time=changed)
        return image

    @staticmethod
    async def _check_image(image_file: File):
        """
        Checks that the image is being opened, is in a valid format and also not oversized
        If there are some problems with opening or format with image file raise APIImageWrongFormat exception
        If image file's size more than max_size from .env raise APIImageMaxSizeExceeded exception
        :param image_file: File
        :return: None
        """
        try:
            image = Image.open(image_file)
        except UnidentifiedImageError as un_im_er:
            raise APIImageWrongFormat() from un_im_er
        if image.format not in ["JPEG", "JPG", "PNG"]:
            raise APIImageWrongFormat()
        image_size = len(image.fp.read())
        max_size = int(os.environ.get("IMAGE_MAX_SIZE")) * 1024 * 1024
        if image_size > max_size:
            raise APIImageMaxSizeExceeded(max_size)
