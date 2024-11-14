from datetime import datetime, timedelta
from pathlib import Path

import requests
from msgspec import json

from cards.card import Card, VirtualCard
from cards.utils import should_skip_card


def process_scryfall_dump():
    name = find_or_get_scryfall_dump()

    with open(name) as file:
        content = file.read()
        cards_json = json.decode(content)

    cards: list[VirtualCard] = []
    current_id = 0

    for card_json in cards_json:
        if should_skip_card(card_json):
            continue

        card = Card.from_scryfall_json(card_json)

        for face in card.faces:
            abstraction = VirtualCard.from_card(current_id, card, face)
            cards.append(abstraction)
            current_id += 1

    return cards


def write_cards_json(cards: list[VirtualCard], name="cards.experimental.json"):
    data = {
        "scryfall_base_uri": "https://scryfall.com/card",
        "scryfall_image_base_uri": "https://cards.scryfall.io",
        "cards": cards,
    }

    with open(name, "wb") as file:
        file.write(json.encode(data))


def find_or_get_scryfall_dump() -> str:
    directory = Path(".cache")
    directory.mkdir(exist_ok=True)

    match should_update_cache(directory):
        case True, None:
            return download_scryfall_dump()
        case False, file_name:
            return file_name


CacheResult = tuple[True, None] | tuple[False, str]


def should_update_cache(dir: Path) -> CacheResult:
    files = list(dir.glob("oracle-cards-*.json"))

    if not files:
        return True, None

    latest = max(files, key=lambda x: x.stat().st_mtime)
    mod_time = datetime.fromtimestamp(latest.stat().st_mtime)
    age = datetime.now() - mod_time

    # Only update dump every ~5 days
    if age < timedelta(days=5):
        return False, latest.as_posix()

    return True, None


# https://scryfall.com/docs/api/bulk-data
def download_scryfall_dump() -> str:
    BULK_URI = "https://api.scryfall.com/bulk-data"
    response = requests.get(BULK_URI).json()

    download_uri = ""

    for each in response["data"]:
        if each["type"] == "oracle_cards":
            download_uri = each["download_uri"]

    file_name = download_uri.split("/")[-1]
    file_name = f".cache/{file_name}"

    dump = requests.get(download_uri).text

    with open(file_name, "w") as file:
        file.write(dump)

    return file_name
