import string


def label_prompt(context: str, choices: list[str]) -> str:
    options = "\n".join(
        f"{label} = {choice}" for label, choice in zip(string.ascii_uppercase, choices)
    )
    return (
        "Choose the best option for the context below. Reply with exactly one label "
        "and no explanation.\n\n"
        f"Context:\n{context}\n\nAllowed outputs:\n{options}\n\nLabel:"
    )
