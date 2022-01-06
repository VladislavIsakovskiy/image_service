import glob
import ntpath
import os
from typing import List

from image_service.errors import APIImageNotDeleted, APIImageNotFound
from image_service.schemas.images import Image

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_FOLDER = os.path.join(CURRENT_DIR, "..", "..", "images")


class ImageService:
    def get_images(self) -> list[Image]:
        images = []
        relevant_extensions = ("*.png", "*.jpg")
        image_paths = self.get_all_relevant_image_paths(relevant_extensions)
        for image_path in image_paths:
            image = self.generate_image(image_path)
            images.append(image)
        return images

    def get_image_info(self, image_name: str) -> Image:
        image_path = self.get_image_path(image_name)
        return self.generate_image(image_path)

    def delete_image(self, image_name: str) -> str:
        image_path = self.get_image_path(image_name)
        os.remove(image_path)
        if os.path.exists(image_path):
            raise APIImageNotDeleted(image_name)
        return f"Image {image_name} deleted successfully!"

    @staticmethod
    def get_image_path(image_name: str) -> str:
        image_path = os.path.join(IMAGES_FOLDER, image_name)
        if not os.path.exists(image_path):
            raise APIImageNotFound(image_name)
        return image_path

    @staticmethod
    def get_all_relevant_image_paths(relevant_extensions: tuple) -> List[str]:
        image_paths = []
        for ext in relevant_extensions:
            image_paths.extend(glob.glob(os.path.join(IMAGES_FOLDER, ext)))
        return image_paths

    @staticmethod
    def generate_image(image_path: str) -> Image:
        image_name = ntpath.basename(image_path)
        byte_size = os.stat(image_path).st_size
        mb_size = round(byte_size / (1024 * 1024), 2)
        str_size = f"{mb_size} MB"
        changed = os.path.getmtime(image_path)
        image = Image(name=image_name, size=str_size, last_change_time=changed)
        return image
