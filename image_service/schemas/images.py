from typing import List

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic.schema import datetime  # pylint: disable=no-name-in-module


class Image(BaseModel):  # pylint: disable=too-few-public-methods
    name: str
    size: str
    last_change_time: datetime


class ImagesOut(BaseModel):  # pylint: disable=too-few-public-methods
    images: List[Image]
