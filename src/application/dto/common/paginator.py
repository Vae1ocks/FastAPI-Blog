from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    offset: int
    limit: int
