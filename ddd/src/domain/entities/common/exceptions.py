class ShortTitleLengthException(Exception):
    def __init__(self, min_length: int):
        super().__init__(f"Title must contain at least {min_length} characters.")


class LongTitleLengthException(Exception):
    def __init__(self, max_length: int):
        super().__init__(f"Title must be a maximum of {max_length} characters.")
