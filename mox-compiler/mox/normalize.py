import re


def normalize(input: str):
    input = input.lower()
    input = re.compile(r".*\s?—\s").sub("", input)
    input = re.compile(r"\([^)]+\)").sub("", input)

    # Special cases
    input = input.replace("this spell", "[[card]]")
    input = input.replace("this creature", "[[card]]")
    input = input.replace("this aura", "[[card]]")
    input = input.replace("this enchantment", "[[card]]")
    input = input.replace("this artifact", "[[card]]")
    input = input.replace("this land", "[[card]]")

    input = input.replace("this card", "[[card]]")

    return input


def mask_name(input: str, name: str):
    for part in [name] + name.split(","):
        input = input.replace(part, "[[card]]")

    return input
