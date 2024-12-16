from typing import AsyncGenerator

from llama_cpp import Llama


class LLMInteractionService:
    def __init__(self, llm: Llama):
        """
        Initialize the LLM interaction service with a Llama instance.

        :param llm: An instance of Llama for model interactions
        """
        self.llm = llm

    def generate_response(self, history: list[dict[str, str]], max_tokens: int = 200, stop: list = None) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM based on the given prompt.

        :param history: The history of messages to send to the model
        :param max_tokens: Maximum number of tokens to generate
        :param stop: List of sequences where the API will stop generation
        :return: An asynchronous generator yielding parts of the response as they are generated
        """
        for chunk in self.llm.create_chat_completion(
            messages=history,
            max_tokens=max_tokens,
            stop=stop or [],
            stream=True
        ):
            yield chunk['choices'][0]['delta'].get('content', '')
