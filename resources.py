from pathlib import Path


class Resources:
    def __init__(self):
        self.prompts = Prompts()

        # BNF grammars for restricted sampling.
        # - space_after_comma_no_comments.txt:
        #   enforces valid Prolog (YAP syntax) with spaces after commas and no comments
        # - space_after_comma_no_comments_two_blocks.txt:
        #   additionally enforces that all rules and facts come before all queries.
        self.grammars = read_directory("grammars")

        # Example texts for converting to Prolog.
        self.examples = read_directory("examples")


class Prompts:
    def __init__(self):
        # A prompt for generating Prolog programs from texts.
        self.to_prolog = read_prompt("to_prolog")

        # Text, converted from Prolog with this prompt, will generally follow the
        # structure of the program. For example, each Prolog rule, fact, and query will
        # become a separate sentence. Also, placeholder variables, such as person1,
        # will be retained.
        self.from_prolog = read_prompt("from_prolog")

        # A prompt for generating natural written-by-human-like texts from Prolog
        # programs.
        self.from_prolog_creative = read_prompt("from_prolog_creative")

        # A prompt for fixing Prolog interpreter warnings and errors.
        self.autocorrect = read_prompt("autocorrect")


def read_prompt(name: str) -> str:
    return (Path("system_prompts") / f"{name}.txt").read_text()


def read_directory(collection: str) -> dict[str, str]:
    return {path.stem: path.read_text() for path in Path(collection).iterdir()}
