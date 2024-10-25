from typing import Optional

import msgspec

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


def extract_card_fields(
    card: dict,
    sid: Optional[str] = None,
    image: Optional[str] = None,
    formats: Optional[str] = None,
):
    name: str = card["name"]

    sid = sid or card["id"]

    image = image or card["image_uris"]["normal"]
    image = extract_image_fragments(image)

    formats = formats or extract_format_legality(card)

    data = {
        # Checked fields
        "sid": sid,
        "name": name,
        "image": image,
        "formats": formats,
        #
        # Fields that are quaranteed to be set
        "mana": card["mana_cost"],
        "oracle": card["oracle_text"],
        "type": card["type_line"],
    }

    # Fields that might be set
    optional = {"flavor": "flavor_text", "power": "power", "toughness": "toughness"}

    for key, card_key in optional.items():
        if card_key in card:
            data[key] = card[card_key]

    return data


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


def process_scryfall_dump(FILE: str):
    with open(FILE) as file:
        content = file.read()
        cards_json = msgspec.json.decode(content)

    cards = []

    for card in cards_json:
        if should_skip_card(card):
            continue

        match card.get("card_faces"):
            case None:
                card = extract_card_fields(card)
                cards.append(card)

            case [front, back]:
                # Faces don't have individual scryfall ids or legalities
                sid = card["id"]
                formats = extract_format_legality(card)

                # Some faces don't have individual images
                image = card.get("image_uris", {}).get("normal")

                front = extract_card_fields(front, sid, image, formats)
                back = extract_card_fields(back, sid, image, formats)

                cards.append(front)
                cards.append(back)

            case faces:
                raise ValueError(
                    f"Too many faces: {len(faces)}. Expected {{1,2}} faces."
                )

    return cards
