from os import environ
from typing import Literal

from openai import OpenAI, omit
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from resources import Prompts

Effort = Literal["low", "medium", "high"] | None


class LLM:
    def __init__(self, client: OpenAI, prompts: Prompts, model: str):
        self._client = client
        self._prompts = prompts
        self._model = model

    def convert_to_prolog(
        self, text: str, temperature: float, effort: Effort, grammar: str | None = None
    ) -> ChatCompletionMessage:
        return self._make_request(
            [
                ChatCompletionSystemMessageParam(
                    content=self._prompts.to_prolog, role="system"
                ),
                ChatCompletionUserMessageParam(content=text, role="user"),
            ],
            temperature,
            effort,
            grammar,
        )

    def convert_from_prolog(
        self,
        prolog: str,
        temperature: float,
        effort: Effort,
        language: str,
        is_creative: bool,
    ) -> ChatCompletionMessage:
        prompt = (
            self._prompts.from_prolog_creative
            if is_creative
            else self._prompts.from_prolog
        )
        prompt = prompt.format(language)

        return self._make_request(
            [
                ChatCompletionSystemMessageParam(content=prompt, role="system"),
                ChatCompletionUserMessageParam(content=prolog, role="user"),
            ],
            temperature,
            effort,
        )

    def autocorrect(
        self,
        prolog: str,
        stderr: str,
        temperature: float,
        effort: Effort,
        grammar: str | None,
    ) -> ChatCompletionMessage:
        prompt = self._prompts.autocorrect.format(
            self._prompts.to_prolog,
            prolog,
            stderr,
        )
        return self._make_request(
            [ChatCompletionSystemMessageParam(content=prompt, role="system")],
            temperature,
            effort,
            grammar,
        )

    def _make_request(
        self,
        messages: list[
            ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam
        ],
        temperature: float,
        effort: Effort,
        grammar: str | None = None,
    ) -> ChatCompletionMessage:
        extra_body = {}

        if grammar:
            extra_body = dict(structured_outputs=dict(grammar=grammar))

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            reasoning_effort=effort or omit,
            extra_body=extra_body,
        )

        return response.choices[0].message


# Self-hosted LLM.
class ModalLLM(LLM):
    def __init__(self, prompts: Prompts):
        client = OpenAI(
            base_url="https://kharacternyk--prolog-llm-serve.modal.run/v1",
            api_key="",
            default_headers={
                "Modal-Key": environ["MODAL_KEY"],
                "Modal-Secret": environ["MODAL_SECRET"],
            },
        )
        super().__init__(client, prompts, "")


# OpenAI-hosted LLM.
class OpenAILLM(LLM):
    def __init__(self, prompts: Prompts, model: str):
        super().__init__(OpenAI(), prompts, model)
