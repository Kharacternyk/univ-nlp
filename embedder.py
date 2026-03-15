from openai import OpenAI


class Embedder:
    def __init__(self):
        self._client = OpenAI()

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            input=text,
            model="text-embedding-3-large",
            encoding_format="float",
        )
        return response.data[0].embedding
