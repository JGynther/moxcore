from dataclasses import asdict, dataclass, fields
from functools import wraps
from typing import Optional


def dataclass_ignore_unknown_params(cls: type) -> type:
    init = cls.__init__

    @wraps(init)
    def __init__(self, *args, **kwargs):
        class_fields = fields(cls)
        field_names = {field.name for field in class_fields}
        known_kwargs = {k: v for k, v in kwargs.items() if k in field_names}
        init(self, *args, **known_kwargs)

    cls.__init__ = __init__
    return cls


@dataclass_ignore_unknown_params
@dataclass(frozen=True)
class CardFace:
    name: str
    mana_cost: str
    oracle_text: str
    type_line: str

    image: str

    flavor_text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None


# To avoid circular import as utils needs CardFace
from cards.utils import extract_format_legality, extract_image_fragments  # noqa: E402


@dataclass
class Card:
    scryfall_id: str
    formats: str
    faces: list[CardFace]

    @classmethod
    def from_scryfall_json(cls, card: dict) -> "Card":
        raw_faces = card.get("card_faces", [card])
        parent_image = card.get("image_uris", {}).get("normal")

        faces = []
        for face in raw_faces:
            image = parent_image or face["image_uris"]["normal"]
            image = extract_image_fragments(image)
            faces.append(CardFace(image=image, **face))

        scryfall_id = card["id"]
        formats = extract_format_legality(card)

        return cls(scryfall_id, formats, faces)


@dataclass
class VirtualCard:
    """
    Representation of a Card used for similarity search.
    Differs from Scryfall's card objects by considering each face of a card separately.
    """

    id: int
    scryfall_id: str
    formats: str

    name: str
    mana_cost: str
    oracle_text: str
    type_line: str

    image: str

    flavor_text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None

    neighbours: Optional[dict[str, list[int]]] = None

    @classmethod
    def from_card(cls, id: int, card: Card, face: CardFace):
        return cls(id, card.scryfall_id, card.formats, **asdict(face))
