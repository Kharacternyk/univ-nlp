from datetime import datetime
from os import environ
from pathlib import Path
from shutil import copyfile

from dotenv import load_dotenv

from embedder import Embedder
from llm import OpenAILLM
from resources import Prompts

load_dotenv()

now = datetime.now()
output_directory = Path("generated") / f"{now.hour}-{now.minute:02}"
output_directory.mkdir(parents=True)

input_file = Path("input.txt")
copyfile(input_file, output_directory / "input.txt")

prompts = Prompts()

llm_from_prolog = OpenAILLM(prompts, "gpt-5.4")
llm_to_prolog = llm_from_prolog

original_text = input_file.read_text()

embedder = Embedder()
original_embedding = embedder.embed(original_text)

effort = environ.get("EFFORT", "medium")

response = llm_to_prolog.convert_to_prolog(original_text, 1, effort)
prolog = response.content

assert prolog
(output_directory / "program.pro").write_text(prolog)

stripped_prolog = ""

for line in prolog.splitlines():
    if "%" not in line:
        stripped_prolog += line + "\n"
        continue

    line = line.split("%")[0].rstrip()

    if line:
        stripped_prolog += line + "\n"

(output_directory / "stripped.pro").write_text(stripped_prolog)

for index in range(3):
    response = llm_from_prolog.convert_from_prolog(
        stripped_prolog, 1, effort, "Ukrainian", True
    )
    generated_text = response.content

    assert generated_text

    generated_embedding = embedder.embed(generated_text)

    similarity = 0

    # Embeddings are pre-normalized to unit length
    for a, b in zip(original_embedding, generated_embedding):
        similarity += a * b

    similarity = round(similarity * 100)

    file_name = f"generated_{index + 1}_similarity_{similarity}.txt"

    (output_directory / file_name).write_text(generated_text)
