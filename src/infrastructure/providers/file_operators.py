from datetime import datetime, UTC
from typing import BinaryIO

from PIL import Image, UnidentifiedImageError
from pathlib import Path
import aiofiles

from application.errors.common.validation import FileNotImageError
from application.providers.file_operators import ImageChecker, ImageLoader


class ImageCheckerImpl(ImageChecker):
    @staticmethod
    def check(file: BinaryIO) -> None:
        try:
            image = Image.open(file)
            image.verify()
        except UnidentifiedImageError as e:
            raise FileNotImageError()


class FileSystemImageLoader(ImageLoader):
    def __init__(self, directory: str, file_name_patter: str):
        self.directory = Path(directory)
        self.file_name_pattern = file_name_patter

    async def __call__(self, image: BinaryIO):
        path = Path(self.directory)
        file_extension = Path(image.filename).suffix
        timestamp = datetime.now(UTC).strftime(
            self.file_name_pattern,
        )
        filepath = path / f"{timestamp}{file_extension}"

        async with aiofiles.open(filepath, "wb") as _file:
            contents = image.read()
            await _file.write(contents)

        return str(filepath)
