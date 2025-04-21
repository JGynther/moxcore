import re

FLAVOR = r"^[^—]*—\s"
REMINDER = r"\([^)]+\)"
combined = re.compile(rf"{FLAVOR}|{REMINDER}")
this = re.compile(r"\b(this (?:spell|creature|aura|enchantment|artifact|land|card|token))\b")


def normalize(input: str, name: str):
    input = mask_name(input, name)

    input = input.lower()
    input = combined.sub("", input)
    input = this.sub("[[card]]", input)

    return input


def mask_name(input: str, name: str):
    for part in [name] + name.split(","):
        input = input.replace(part, "[[card]]")

    return input
