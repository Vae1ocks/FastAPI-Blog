from fastapi import UploadFile

from application.dto.other.file import FileDTO


class UploadFileToDTOMapper:
    @staticmethod
    def to_dto(file: UploadFile) -> FileDTO:
        return FileDTO(
            file=file.file,
            filename=file.filename,
            size=file.size,
        )
