class LLMRegistry:
    def __init__(self):
        self.models = {}

    def register(self, name, llm):
        self.models[name] = llm

    def get(self, name):
        return self.models[name]