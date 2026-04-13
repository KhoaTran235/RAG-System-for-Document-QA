from orchestration.langgraph.nodes import Nodes
from orchestration.langgraph.graph import build_graph
from orchestration.langgraph.runner import LangGraphRAG

# ===== core components (của bạn) =====
rewriter = ...
retriever = ...
reranker = ...
prompt_builder = ...
llm = ...

# ===== build nodes =====
nodes = Nodes(
    rewriter=rewriter,
    retriever=retriever,
    reranker=reranker,
    prompt_builder=prompt_builder,
    llm=llm
)

# ===== build graph =====
graph = build_graph(nodes)

# ===== runner =====
rag = LangGraphRAG(graph)

# ===== run =====
answer = rag.run("What is RAG?")
print(answer)