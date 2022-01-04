import glob
import ntpath
import os
from typing import List

from image_service.schemas.images import Image


class ImageService:
    def get_images(self) -> list[Image]:
        images = []
        relevant_extensions = ("*.png", "*.jpg")
        image_paths = self.get_all_relevant_image_paths(relevant_extensions)
        for image_path in image_paths:
            image = self.generate_image(image_path)
            images.append(image)
        return images

    @staticmethod
    def get_all_relevant_image_paths(relevant_extensions: tuple) -> List[str]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "..", "..", "images")
        image_paths = []
        for ext in relevant_extensions:
            image_paths.extend(glob.glob(os.path.join(image_path, ext)))
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
