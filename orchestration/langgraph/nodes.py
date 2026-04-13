class Nodes:
    def __init__(self, rewriter, retriever, reranker, prompt_builder, llm):
        self.rewriter = rewriter
        self.retriever = retriever
        self.reranker = reranker
        self.prompt_builder = prompt_builder
        self.llm = llm

    # 1. Rewrite
    def rewrite(self, state):
        if not self.rewriter:
            return {"rewritten_query": state["query"]}

        new_query = self.rewriter.rewrite(state["query"])
        return {"rewritten_query": new_query}

    # 2. Retrieve
    def retrieve(self, state):
        query = state.get("rewritten_query", state["query"])
        docs = self.retriever.retrieve(query)

        return {"documents": docs}

    # 3. Rerank
    def rerank(self, state):
        query = state.get("rewritten_query", state["query"])
        docs = state["documents"]

        reranked = self.reranker.rerank(query, docs)
        return {"documents": reranked}

    # 4. Generate
    def generate(self, state):
        query = state.get("rewritten_query", state["query"])
        docs = state["documents"]

        prompt = self.prompt_builder.build(query=query, documents=docs)
        answer = self.llm.generate(prompt)

        return {"answer": answer}