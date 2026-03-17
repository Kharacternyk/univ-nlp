from typing import cast

from dotenv import load_dotenv
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

from llm import LLM, Effort, ModalLLM, OpenAILLM
from resources import Resources
from utils import run_prolog, split_prolog

# Loads environment variables such as OPENAI_API_KEY from the .env file.
load_dotenv()

# Text files.
resources = cache_resource(Resources)()


# LLM for converting to Prolog.
@cache_resource
def get_llm_to_prolog() -> LLM:
    # Change models as needed
    return ModalLLM(resources.prompts)


llm_to_prolog = get_llm_to_prolog()


# LLM for converting from Prolog.
@cache_resource
def get_llm_from_prolog() -> LLM:
    # Change models as needed
    return OpenAILLM(resources.prompts, "gpt-5-mini")


llm_from_prolog = get_llm_from_prolog()


# Run Prolog through SWI interpreter and display output.
# Returns all errors and warnings.
def render_prolog_output(rules: str, queries: str) -> str:
    return run_prolog(rules, queries, lambda query: code(query, language="prolog"))[1]


to_prolog, from_prolog = tabs(["To Prolog", "From Prolog"])

# Converting to Prolog user interface section (tab).
with to_prolog:
    default_input = next(iter(resources.examples))
    text = text_area("Input text", key="text", height=200)

    with container(horizontal=True):
        for index, example in enumerate(resources.examples.values()):

            def set_query(text=example):
                session_state.text = text

            button(f"Example {index + 1}", on_click=set_query)

    grammar_name = selectbox("Grammar", ["None"] + list(resources.grammars.keys()))
    grammar = resources.grammars.get(grammar_name)

    # High reasoning effort generally takes a very long time to complete, so
    # it's not among the available options.
    effort = selectbox("Reasoning effort", ["Low", "Medium"], index=1).lower()
    effort = cast(Effort, effort)

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

    # If any of the three conversion buttons is pressed
    if do_run or do_autocorrect or do_convert:
        response = llm_to_prolog.convert_to_prolog(
            text,
            temperature,
            effort,
            grammar,
        )

        with expander("Reasoning"):
            raw(getattr(response, "reasoning_content", ""))

        prolog = response.content

        assert prolog

        if do_convert:
            # The "Convert" button just displays the generated Prolog program.
            code(prolog, language="prolog")
        else:
            # The "Convert & Run" buttons run the program.
            rules, queries = split_prolog(prolog)

            code(rules, language="prolog")

            stderr = render_prolog_output(rules, queries)

            # The "Convert & Run & Autocorrect" button tries to regenerate the
            # program to fix interpreter warnings and errors.
            if stderr and do_autocorrect:
                response = llm_to_prolog.autocorrect(
                    prolog, stderr, temperature, effort, grammar
                )

                divider()

                with expander("Reasoning"):
                    raw(getattr(response, "reasoning_content", ""))

                prolog = response.content

                assert prolog

                rules, queries = split_prolog(prolog)

                code(rules, language="prolog")

                render_prolog_output(rules, queries)


# Converting from Prolog user interface section (tab).
with from_prolog:
    prolog = text_area("Input text", key="prolog", height=200)
    prompt_type = selectbox("Prompt type", ["Verbatim", "Creative"])
    language = selectbox("Language", ["English", "Ukrainian"])

    if button("Convert", width="stretch", type="primary"):
        # GPT-5-mini does not support reasoning and temperatures other than 1.
        response = llm_from_prolog.convert_from_prolog(
            prolog,
            1.0,
            "medium",
            language,
            prompt_type == "Creative",
        )
        raw(response.content)
