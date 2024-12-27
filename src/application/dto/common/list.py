from dataclasses import dataclass

from application.common.enums.sort_order import SortOrder
from application.dto.common.paginator import Pagination


@dataclass(frozen=True, slots=True)
class ListObjectsDTO:
    paginator: Pagination
    order: SortOrder = SortOrder.ASC
