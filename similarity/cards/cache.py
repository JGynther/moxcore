import pickle
import typing as T
from pathlib import Path
from time import time

import requests
from cards.card import VirtualCard
from cards.process_dump import process_scryfall_dump
from msgspec import json
from search.utils import timer

CACHE = Path(".cache")
DATA = CACHE / "data.pkl"
META = CACHE / ".meta.json"
TTL_IN_S = 432_000  # 5 days


@timer
def get_scryfall_data_from_cache() -> list[VirtualCard]:
    refresh_cache_if_needed()
    return pickle.loads(DATA.read_bytes())


class Metadata(T.TypedDict):
    timestamp: float
    raw_file: str


def write_metadata(raw_file_name: str):
    data = {"timestamp": time(), "raw_file": raw_file_name}
    META.write_bytes(json.encode(data))


def get_metadata() -> Metadata | None:
    if not META.exists():
        return None

    return json.decode(META.read_bytes())


def refresh_cache_if_needed():
    CACHE.mkdir(exist_ok=True)
    metadata = get_metadata()
    current_time = time()

    if DATA.exists() and metadata:
        if current_time - metadata["timestamp"] < TTL_IN_S:
            return print("Using cached data.")

    print("Downloading new Scryfall dump.")

    file_name = download_scryfall_dump()
    processed = process_scryfall_dump(file_name)
    DATA.write_bytes(pickle.dumps(processed))
    write_metadata(file_name)


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
