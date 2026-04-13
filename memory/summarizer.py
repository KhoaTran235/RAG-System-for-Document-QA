from typing import List
from generation.llm.base import BaseLLM
from generation.prompt.prompt_builder import PromptBuilder
from schemas.message import Message
from schemas.summary import Summary

class Summarizer:
    def __init__(self, llm: BaseLLM, prompt_builder: PromptBuilder):
        self.llm = llm
        self.prompt_builder = prompt_builder
    
    def summarize(self, chat_history: List[Message], prev_summary: Summary):
        # Combine the chat history and previous summary into a single prompt
        prompt = self.prompt_builder.build_summary_prompt(chat_history, prev_summary)
        
        # Use the LLM to generate a summary
        response = self.llm.generate(
            prompt,
            response_mime_type="application/json",
            response_json_schema=Summary.model_json_schema()
        )
        new_chat_history = chat_history[:-4] if len(chat_history) > 4 else chat_history # Keep the last 4 messages for context
        new_summary = Summary.model_validate_json(response.text)
        return new_summary, new_chat_history
    
if __name__ == "__main__":
    # Example usage
    from generation.llm.clients.gemini_client import GeminiClient
    from generation.prompt.prompt_builder import PromptBuilder
    llm = GeminiClient(model_name="gemini-3.1-flash-lite-preview")
    prompt_builder = PromptBuilder()
    summarizer = Summarizer(llm=llm, prompt_builder=prompt_builder)

    chat_history = [
        Message(role="user", content="What is the capital of France?"),
        Message(role="assistant", content="The capital of France is Paris."),
        Message(role="user", content="What about Germany?"),
        Message(role="assistant", content="The capital of Germany is Berlin."),
        Message(role="user", content="And Italy?"),
        Message(role="assistant", content="The capital of Italy is Rome.")
    ]
    prev_summary = Summary(content="The user asked about the capitals of France, Germany. The assistant provided the answers: Paris for France, Berlin for Germany.")
    
    new_summary, new_chat_history = summarizer.summarize(chat_history=chat_history, prev_summary=prev_summary)
    print("New Summary:", new_summary.model_dump_json())