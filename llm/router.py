class LLMRouter:
    def __init__(self, registry, routing_config):
        self.registry = registry
        self.routing_config = routing_config

    def generate(self, task: str, prompt: str, **kwargs):
        model_name = self.routing_config[task]
        llm = self.registry.get(model_name)
        return llm.generate(prompt, **kwargs)
    
    def count_tokens(self, task: str, text: str):
        model_name = self.routing_config[task]
        llm = self.registry.get(model_name)
        return llm.count_tokens(text)