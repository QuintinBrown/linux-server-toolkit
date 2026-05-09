# abstract plugin method

from abc import ABC, abstractmethod

class BasePlugin(ABC):
    name = "Base"

    @abstractmethod
    def commands(self):
        pass