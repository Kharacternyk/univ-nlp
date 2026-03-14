from datetime import datetime
from pathlib import Path
from shutil import copyfile

from dotenv import load_dotenv

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

response = llm_to_prolog.convert_to_prolog(original_text, 1, "medium")
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
        stripped_prolog, 1, "medium", "Ukrainian", True
    )
    generated_text = response.content

    assert generated_text

    (output_directory / f"generated_{index + 1}.txt").write_text(generated_text)
