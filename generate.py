from pathlib import Path

from dotenv import load_dotenv

from llm import OpenAILLM
from resources import Prompts

load_dotenv()

prompts = Prompts()

llm_from_prolog = OpenAILLM(prompts, "gpt-5.4")
llm_to_prolog = llm_from_prolog

original_text = Path("input.txt").read_text()

response = llm_to_prolog.convert_to_prolog(original_text, 1, "medium")
prolog = response.content

assert prolog
(Path("generated") / "prolog.txt").write_text(prolog)

stripped_prolog = ""

for line in prolog.splitlines():
    if "%" not in line:
        stripped_prolog += line
        continue

    line = line.split("%")[0].rstrip()

    if line:
        stripped_prolog += line + "\n"

(Path("generated") / "stripped_prolog.txt").write_text(stripped_prolog)

for index in range(3):
    response = llm_from_prolog.convert_from_prolog(
        stripped_prolog, 1, "medium", "Ukrainian", True
    )
    generated_text = response.content

    assert generated_text

    (Path("generated") / f"{index + 1}.txt").write_text(generated_text)
