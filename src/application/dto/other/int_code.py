from dataclasses import dataclass


@dataclass(frozen=True, eq=False, slots=True)
class ConfirmationCodesDTO:
    user_id: int
    expected_code: int
    provided_code: int
