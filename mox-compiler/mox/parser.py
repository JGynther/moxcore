from mox.ability import parse_ability
from mox.data_types import Card
from mox.keywords import KEYWORDS
from mox.normalize import mask_name, normalize


def parse(input: str, name: str, type: str):
    input = mask_name(input, name)
    input = normalize(input)
    is_spell = type == "Instant" or type == "Sorcery"

    abilities = []
    keywords = list(set(KEYWORDS.findall(input)))

    for paragraph in input.split("\n"):
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if (
            not KEYWORDS.sub("", paragraph)
            .replace(",", "")
            .replace(".", "")
            .replace(";", "")
            .strip()
        ):
            continue

        abilities.append(parse_ability(paragraph, is_spell))

    return Card(name, type, abilities, list(keywords))
