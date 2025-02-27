import re


def normalize(input: str):
    input = input.lower()
    input = re.compile(r".*\s?—\s").sub("", input)
    input = re.compile(r"\([^)]+\)").sub("", input)
    input = input.replace("this spell", "[[card]]")
    input = input.replace("this creature", "[[card]]")
    input = input.replace("this aura", "[[card]]")

    return input


def mask_name(input: str, name: str):
    for part in [name] + name.split(","):
        input = input.replace(part, "[[card]]")

    return input
