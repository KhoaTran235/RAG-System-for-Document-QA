from typing import Dict, Type
from generation.llm.base import BaseLLM

class LLMRegistry:
    def __init__(self):
        self.models: Dict[str, Type[BaseLLM]] = {}

    def register(self, name: str, llm: Type[BaseLLM]):
        self.models[name] = llm

    def get(self, name: str) -> Type[BaseLLM]:
        return self.models[name]
    
    def list(self):
        return list(self.models.keys())