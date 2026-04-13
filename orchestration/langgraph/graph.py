from langgraph.graph import StateGraph, END
from orchestration.langgraph.state import RAGState
from orchestration.langgraph.nodes import Nodes


def build_graph(nodes: "Nodes"):
    builder = StateGraph(RAGState)

    # add nodes
    builder.add_node("rewrite", nodes.rewrite)
    builder.add_node("retrieve", nodes.retrieve)
    builder.add_node("rerank", nodes.rerank)
    builder.add_node("generate", nodes.generate)

    # entry
    builder.set_entry_point("rewrite")

    # edges
    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("retrieve", "rerank")
    builder.add_edge("rerank", "generate")
    builder.add_edge("generate", END)

    return builder.compile()