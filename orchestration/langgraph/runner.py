class LangGraphRAG:
    def __init__(self, graph):
        self.graph = graph

    def run(self, query: str):
        result = self.graph.invoke({
            "query": query
        })
        return result["answer"]