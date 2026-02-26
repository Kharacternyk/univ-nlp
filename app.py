from glob import glob
from os import environ
from subprocess import run
from tempfile import NamedTemporaryFile

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from streamlit import (
    button,
    cache_resource,
    code,
    columns,
    container,
    divider,
    expander,
    selectbox,
    session_state,
    slider,
    tabs,
    text_area,
)
from streamlit import (
    text as raw,
)

load_dotenv()


@cache_resource
def modal():
    return OpenAI(
        base_url="https://kharacternyk--prolog-llm-serve.modal.run/v1",
        api_key="",
        default_headers={
            "Modal-Key": environ["MODAL_KEY"],
            "Modal-Secret": environ["MODAL_SECRET"],
        },
    )


@cache_resource
def openai():
    return OpenAI()


def read_file(path):
    with open(path) as file:
        return file.read()


@cache_resource
def system_prompt_to_prolog():
    return read_file("system_prompts/to_prolog.txt")


@cache_resource
def system_prompt_from_prolog():
    return read_file("system_prompts/from_prolog.txt")


@cache_resource
def system_prompt_from_prolog_creative():
    return read_file("system_prompts/from_prolog_creative.txt")


@cache_resource
def system_prompt_autocorrect():
    return read_file("system_prompts/autocorrect.txt")


@cache_resource
def grammars():
    grammars: list[tuple[str, str | None]] = [("None", None)]

    for path in glob("grammars/*.txt"):
        grammars.append((path, read_file(path)))

    return grammars


@cache_resource
def examples():
    examples = []

    for path in glob("examples/*.txt"):
        examples.append(read_file(path))

    return examples


def split_prolog(prolog):
    try:
        first_query_index = prolog.index("?-")
    except ValueError:
        first_query_index = len(prolog)

    rules = prolog[:first_query_index]
    queries = prolog[first_query_index:]

    return rules, queries


def render_prolog_output(rules, queries):
    all_stderr = ""

    with NamedTemporaryFile("w") as file:
        file.write(rules)
        file.flush()

        for query in queries.splitlines():
            code(query, language="prolog")

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
                code(stdout)
            if stderr:
                code(stderr)
                all_stderr += stderr

    return all_stderr


to_prolog, from_prolog = tabs(["To Prolog", "From Prolog"])

with to_prolog:
    default_input = str(examples()[0])
    text = text_area("Input text", key="text", height=200)

    with container(horizontal=True):
        for index, example in enumerate(examples()):

            def set_query(text=example):
                session_state.text = text

            button(f"Example {index + 1}", on_click=set_query)

    grammar_index = selectbox(
        "Grammar", range(len(grammars())), format_func=lambda i: grammars()[i][0]
    )

    if grammar_index > 0:
        extra_body = dict(structured_outputs=dict(grammar=grammars()[grammar_index][1]))
    else:
        extra_body = dict()

    reasoning_effort = selectbox("Reasoning effort", ["Low", "Medium"], index=1).lower()

    temperature = slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.05
    )

    left, center, right = columns(3)

    with left:
        do_autocorrect = button(
            "Convert & Run & Autocorrect", type="primary", width="stretch"
        )
    with center:
        do_run = button("Convert & Run", width="stretch")
    with right:
        do_convert = button("Convert", width="stretch")

    if do_run or do_autocorrect or do_convert:
        response = modal().chat.completions.create(
            model="",
            messages=[
                ChatCompletionSystemMessageParam(
                    content=system_prompt_to_prolog(), role="system"
                ),
                ChatCompletionUserMessageParam(content=text, role="user"),
            ],
            temperature=temperature,
            reasoning_effort=reasoning_effort,
            extra_body=extra_body,
        )
        message = response.choices[0].message

        with expander("Reasoning"):
            raw(message.reasoning_content)

        prolog = message.content

        assert prolog

        if do_convert:
            code(prolog, language="prolog")
        else:
            rules, queries = split_prolog(prolog)

            code(rules, language="prolog")

            all_stderr = render_prolog_output(rules, queries)

            if all_stderr and do_autocorrect:
                system_prompt = system_prompt_autocorrect().format(
                    system_prompt_to_prolog(),
                    prolog,
                    all_stderr,
                )
                response = modal().chat.completions.create(
                    model="",
                    messages=[
                        ChatCompletionSystemMessageParam(
                            content=system_prompt, role="system"
                        ),
                    ],
                    temperature=temperature,
                    reasoning_effort=reasoning_effort,
                    extra_body=extra_body,
                )
                message = response.choices[0].message

                divider()

                with expander("Reasoning"):
                    raw(message.reasoning_content)

                rules, queries = split_prolog(message.content)

                code(rules, language="prolog")

                render_prolog_output(rules, queries)


with from_prolog:
    prolog = text_area("Input text", key="prolog", height=200)
    prompt_type = selectbox("Prompt type", ["Verbatim", "Creative"])
    language = selectbox("Language", ["English", "Ukrainian"])

    if prompt_type == "Verbatim":
        prompt = system_prompt_from_prolog()
    else:
        prompt = system_prompt_from_prolog_creative()

    prompt = prompt.format(language)

    if button("Convert", width="stretch", type="primary"):
        response = openai().chat.completions.create(
            model="gpt-5-mini",
            messages=[
                ChatCompletionSystemMessageParam(content=prompt, role="system"),
                ChatCompletionUserMessageParam(content=prolog, role="user"),
            ],
        )
        message = response.choices[0].message
        raw(message.content)
