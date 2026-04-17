
from typing import List

from generation.prompt.prompt_builder import PromptBuilder
from generation.llm.router import LLMRouter
from schemas.message import Message


class QueryRewriter:
    def __init__(self, llm: LLMRouter):
        self.llm = llm
    
    def rewrite(self, query: Message, chat_history: List[Message]) -> Message:
        # Combine the query and chat history into a single prompt
        # query_content = query.content
        # history_content = "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
        prompt = PromptBuilder.build_rewrite_prompt(query=query, chat_history=chat_history)
        # Use the LLM to rewrite the query
        rewritten_query = self.llm.generate(task="rewrite", prompt=prompt).text
        
        return Message(role="user", content=rewritten_query)
    
if __name__ == "__main__":
    # Example usage
    from generation.llm.clients.gemini_client import GeminiClient
    from generation.prompt.prompt_builder import PromptBuilder
    llm = GeminiClient(model_name="gemma-3-1b-it")
    prompt_builder = PromptBuilder()
    rewriter = QueryRewriter(llm=llm)

    chat_history = [
        Message(role="user", content="What is the capital of France?"),
        Message(role="assistant", content="The capital of France is Paris.")
    ]
    query = Message(role="user", content="What about Germany?")
    new_query = rewriter.rewrite(query=query, chat_history=chat_history)
    print("Rewritten Query:", new_query.content)