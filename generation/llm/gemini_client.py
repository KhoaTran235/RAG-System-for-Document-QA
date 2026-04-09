from dotenv import load_dotenv
import os

from generation.llm.base import BaseLLM
from google import genai
from google.genai import types

load_dotenv()

class GeminiClient(BaseLLM):
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate(self, prompt, **kwargs):
        # call API
        response = self.client.models.generate_content(
            model=self.model_name,
            contents={'text': f'{prompt}'},
            config=types.GenerateContentConfig(
                system_instruction=kwargs.get('system_instruction', None),
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 0.9),
                top_k=kwargs.get('top_k', 40),
                max_output_tokens=kwargs.get('max_output_tokens', 2048),
                response_json_schema=kwargs.get('response_json_schema', None)
            )
        )
        return f"[Google:{self.model_name}] {response.text}"
    
    def generate_stream(self, prompt, **kwargs):
        response = self.client.models.generate_content_stream(
            model=self.model_name,
            contents={'text': f'{prompt}'},
            config=types.GenerateContentConfig(
                system_instruction=kwargs.get('system_instruction', None),
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 0.9),
                top_k=kwargs.get('top_k', 40),
                max_output_tokens=kwargs.get('max_output_tokens', 2048),
                response_json_schema=kwargs.get('response_json_schema', None)
            )
        )
        return response
    
    def count_tokens(self, text):
        return self.client.models.count_tokens(
            model=self.model_name,
            contents=text
        ).total_tokens
    
if __name__ == "__main__":
    # Example usage
    model_name = "gemma-3-1b-it"
    client = GeminiClient(model_name)
    prompt = "What is the capital of France?"

    token_count = client.count_tokens(prompt)
    response = client.generate(prompt, temperature=1.0)
    
    print(f"Token Count: {token_count}")
    print(f"Prompt: {prompt}")
    print(f"Response: {response.text}")

    response_stream = client.generate_stream(prompt, temperature=1.0)
    print("\nStreaming response:")
    for chunk in response_stream:
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
        ):
            parts = chunk.candidates[0].content.parts

            for part in parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)
    