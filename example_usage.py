# example_usage.py

from core.config import load_config

# LLM
from generation.llm.registry import LLMRegistry
from generation.llm.router import LLMRouter
from generation.llm.factory import create_llm

# embedding
from embedding.gemini_embedder import GeminiEmbedder

# load config
config = load_config()

# init registry
registry = LLMRegistry()

# create LLM models from config
for name, model_cfg in config["llm"]["models"].items():
    llm = create_llm(model_cfg)
    registry.register(name, llm)

# init embedder from config
embedding_model_name = config["embedding"]["model_name"]
embedder = GeminiEmbedder(embedding_model_name)

# init router
router = LLMRouter(
    registry=registry,
    routing_config=config["llm"]["routing"]
)

prompt = "What is the capital of France?"
response = router.generate(task="qa", prompt=prompt, system_instruction="You are a funny assistant that always responds in a humorous way.", temperature=1.0)
print(response.text)

embedding_response = embedder.embed_query(prompt, task_type="search")
print(embedding_response)