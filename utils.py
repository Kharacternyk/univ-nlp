from subprocess import run
from tempfile import NamedTemporaryFile
from typing import Callable


# Assuming that queries follow all facts and rules, splits a Prolog program
# into the two blocks.
def split_prolog(prolog: str):
    try:
        first_query_index = prolog.index("?-")
    except ValueError:
        first_query_index = len(prolog)

    rules = prolog[:first_query_index]
    queries = prolog[first_query_index:]

    return rules, queries


# Run Prolog through SWI interpreter.
# Returns combined stderr.
def run_prolog(rules: str, queries: str, display: Callable[[str], None]) -> str:
    all_stderr = ""

    with NamedTemporaryFile("w") as file:
        file.write(rules)
        file.flush()

        for query in queries.splitlines():
            display(query)

            arguments = [
                "swipl",
                "-s",
                file.name,
                "-g",
                query.removeprefix("?-"),
                "-t",
                "halt",
            ]
            result = run(arguments, capture_output=True)

            stdout = result.stdout.decode()
            stderr = result.stderr.decode()

            if stdout:
                display(stdout)
            if stderr:
                display(stderr)
                all_stderr += stderr

    return all_stderr
