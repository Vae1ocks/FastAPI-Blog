from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True, slots=True)
class FileDTO:
    file: BinaryIO
    size: int | None = None
    filename: str | None = None