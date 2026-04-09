from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def generate_stream(self, prompt: str, **kwargs):
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass