from datetime import datetime, UTC
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from pathlib import Path
import aiofiles

from application.providers.file_operators import ImageChecker, ImageLoader
from infrastructure.persistence.alembic.env import config


class ImageCheckerImpl(ImageChecker):
    def __call__(self, file: BytesIO):
        try:
            image = Image.open(file)
            image.verify()
            return True
        except UnidentifiedImageError:
            return False


class FileSystemImageLoader(ImageLoader):
    def __init__(self, settings):
        self.directory = Path(settings.users_profile_images_directory)
        self.file_name_pattern = settings.file_save_time_pattern

    async def __call__(self, image: BytesIO) -> str:
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
