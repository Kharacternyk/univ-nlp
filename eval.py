from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from llm import ModalLLM, OpenAILLM
from resources import Prompts
from utils import run_prolog, split_prolog

load_dotenv()

prompts = Prompts()

llms = {
    "gpt-oss-120b": ModalLLM(prompts),
    "gpt-5-mini": OpenAILLM(prompts, "gpt-5-mini"),
    "gpt-5.4": OpenAILLM(prompts, "gpt-5.4"),
}

now = datetime.now()

with open(f"report-{now.hour}-{now.minute}.csv", "w") as report:
    for case_index, test_case in enumerate(Path("./eval").iterdir()):
        text = (test_case / "input.txt").read_text()
        output = (test_case / "output.txt").read_text()

        print(f">>>> Test case #{case_index + 1}")
        print(">>> Input:")
        print(text)

        print(">>> Expected output:")
        print(output)

        for name, llm in llms.items():
            print(">> LLM:", name)

            for run_index in range(3):
                print(f"> Run #{run_index + 1}")

                response = llm.convert_to_prolog(text, 1, "medium")

                prolog = response.content

                assert prolog

                print(prolog)

                rules, queries = split_prolog(prolog)

                stdout = run_prolog(rules, queries, lambda _: None)[0]

                print(stdout)

                is_success = stdout.strip() == output.strip()

                print(
                    ",".join(
                        map(
                            str,
                            [
                                case_index,
                                name,
                                run_index,
                                is_success,
                            ],
                        )
                    ),
                    file=report,
                )
