from generation.llm.gemini_client import GeminiClient


def create_llm(model_config):
    provider = model_config["provider"]

    if provider == "google":
        return GeminiClient(model_config["model_name"])

    # Future support for other providers can be added here
    # elif provider == "local":
    #     return LocalLLM(model_config["model_name"])

    else:
        raise ValueError(f"Unknown provider: {provider}")