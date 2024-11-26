from random import randint

from application.providers.code_generator import RandomCodeGenerator


class RandomIntegerCodeGenerator(RandomCodeGenerator):
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self):
        return randint(self.min_val, self.max_val)
