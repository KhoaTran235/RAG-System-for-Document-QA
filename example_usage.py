from core.config import load_config

# LLM
from generation.llm.registry import LLMRegistry
from generation.llm.router import LLMRouter
from generation.llm.factory import create_llm

# embedding
from embedding.gemini_embedder import GeminiEmbedder

# schemas
from schemas.message import Message
from schemas.summary import Summary
from schemas.chunk import Chunk

# ingestion
from ingestion.pipeline import IngestionPipeline

# query processing
from query.rewrite import QueryRewriter

# summarization
from memory.summarizer import Summarizer

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

rewriter = QueryRewriter(llm=router)
summarizer = Summarizer(llm=router)

# Chat history and previous summary for testing
chat_history = [
        Message(role="user", content="What is the capital of France?"),
        Message(role="assistant", content="The capital of France is Paris."),
        Message(role="user", content="What about Germany?"),
        Message(role="assistant", content="The capital of Germany is Berlin."),
    ]
prev_summary = Summary(content="The user asked about the capitals of France, Germany. The assistant provided the answers: Paris for France, Berlin for Germany.")

# New query to rewrite and summarize
query = Message(role="user", content="And Italy?")
chat_history.append(query)

print("Starting...")
# Rewrite the query
new_query = rewriter.rewrite(query=query, chat_history=chat_history)
print("Rewritten Query:", new_query.content)

# Summarize the conversation so far
mock_response = "The capital of Italy is Rome."
chat_history.append(Message(role="assistant", content=mock_response))
new_summary, new_chat_history = summarizer.summarize(chat_history=chat_history, prev_summary=prev_summary)

print("New Summary:", new_summary.model_dump_json())
print("New Chat History:")
for msg in new_chat_history:
    print(f"{msg.role}: {msg.content}")
