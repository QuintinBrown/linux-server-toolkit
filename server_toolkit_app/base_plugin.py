# abstract plugin method

from abc import ABC, abstractmethod

class BasePlugin(ABC):
    name = "Base"
    output_lines = []

    def __init__(self, output_func=None):
        self.output_func = output_func or print

    def output(self, text):
        self.output_func(str(text))

    def run(self, cmd):
        pass

    def get_error_code(self, cmd):
        pass

    @abstractmethod
    def commands(self):
        pass