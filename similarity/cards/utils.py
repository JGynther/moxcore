import re

from cards.card import CardFace


def should_skip_card(card: dict) -> bool:
    match card:
        # Remove Alchemy only cards
        case {"games": ["arena"]}:
            return True

        # Remove un(official) cards
        case {"legalities": {"vintage": "not_legal"}}:
            return True

        case {"type_line": type_line} if "Conspiracy" in type_line:
            return True

        case _:
            return False


FORMATS = ["commander", "legacy", "modern", "pauper", "pioneer", "standard", "vintage"]
FORMATS = sorted(FORMATS)  # Double triple making sure alphabetical order is followed

legality_map = {"not_legal": "0", "legal": "1", "banned": "2", "restricted": "3"}


def extract_format_legality(card: dict):
    encoded_formats = ""

    for format_ in FORMATS:
        legality = card["legalities"][format_]
        encoded_formats += legality_map[legality]

    return encoded_formats


def extract_image_fragments(image_uri: str):
    # Splits an image uri like
    # https://cards.scryfall.io/normal/front/8/b/8bc518fc-904e-4e39-aeda-ffb222bfcc82.jpg
    # --> front, 8, b
    [_, _, _, _, side, fragment_a, fragment_b, *_] = image_uri.split("/")

    return f"{side}/{fragment_a}/{fragment_b}"


def normalize_oracle_text(card: CardFace):
    oracle = card.oracle_text
    oracle = oracle.replace(card.name, "this")
    oracle = oracle.lower()

    # FIXME: this should be replaced to use the parser
    oracle = re.sub(r"\([^)]+\)", "", oracle)  # Remove reminder text between ()
    oracle = re.sub(r"\{[^}]*\}", "", oracle)  # Remove symbols?

    # Replace some symbols with defining text
    # FIXME: Scryfall has full english description for symbols
    # text = text.replace("{T}", "tap")
    # text = text.replace("{Q}", "untap")
    # text = text.replace("{E}", "energy")

    return oracle
