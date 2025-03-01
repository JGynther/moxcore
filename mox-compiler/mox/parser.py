from mox.ability import parse_ability
from mox.data_types import Card
from mox.keywords import extract_keywords, is_only_keywords
from mox.normalize import mask_name, normalize


def parse(input: str, name: str, type: str):
    input = mask_name(input, name)
    input = normalize(input)
    is_spell = "Instant" in type or "Sorcery" in type

    abilities = []
    keywords = extract_keywords(input)

    for paragraph in input.split("\n"):
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if is_only_keywords(paragraph, keywords):
            continue

        abilities.append(parse_ability(paragraph, is_spell))

    return Card(name, type, abilities, keywords)
