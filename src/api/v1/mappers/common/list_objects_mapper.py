from application.common.enums.sort_order import SortOrder
from application.dto.common.list import ListObjectsDTO
from application.dto.common.paginator import Pagination


class ListObjectsOrderMapper:
    @staticmethod
    def to_dto(offset: int, limit: int, order: str) -> ListObjectsDTO:
        return ListObjectsDTO(
            paginator=Pagination(offset=offset, limit=limit),
            order=SortOrder(order) if order else SortOrder.ASC
        )