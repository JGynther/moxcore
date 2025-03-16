import typing as T
from dataclasses import dataclass
from enum import Enum


class CardType(Enum):
    ARTIFACT = "artifact"
    BATTLE = "battle"
    CREATURE = "creature"
    ENCHANTMENT = "enchantment"
    INSTANT = "instant"
    KINDRED = "kindred"
    LAND = "land"
    PLANESWALKER = "planeswalker"
    SORCERY = "sorcery"


class Zone(Enum):
    BATTLEFIELD = "battlefield"
    GRAVEYARD = "graveyard"
    EXILE = "exile"
    LIBRARY = "library"
    HAND = "hand"
    STACK = "stack"
    COMMAND = "command"

    # Used when a zone is not relevant
    NULL = "null"


class Player(Enum):
    YOU = "you"
    OPPONENT = "opponent"
    ANY = "any"
    ALL = "all"


@dataclass
class Cost:
    W: int = 0
    U: int = 0
    B: int = 0
    R: int = 0
    G: int = 0
    C: int = 0

    tap: bool = False
    untap: bool = False
    sacrifice: str = ""


type Target = Player | CardType


class EType(Enum):
    """Categories of effects a card can have"""

    # Affects board state
    DESTROY = "destroy"
    EXILE = "exile"
    TOKENS = "tokens"
    COUNTERS = "counters"
    PUT_LAND = "put_land"
    PUT_CREATURE = "put_creature"
    REANIMATE = "reanimate"
    BOUNCE = "bounce"
    BLINK = "blink"

    # Resources
    DRAW = "draw"
    TUTOR = "tutor"
    MANA = "mana"
    LIFE_GAIN = "life_gain"
    DISCARD = "discard"

    # Combat
    DAMAGE = "damage"
    LIFE_LOSS = "life_loss"

    # Change or block effects
    PREVENTION = "prevention"
    REPLACEMENT = "replacement"
    MODIFY_STRENGTH = "modify_strength"

    # Misc
    VOTE = "vote"
    KEYWORD = "keyword"  # keyword followed by cost e.g. "emerge {6}{u}"

    # Fallback
    UNKNOWN = "unknown"


class Effect(T.NamedTuple):
    type: EType
    text: str
    target: str | None = None
    source: Zone | None = None
    destination: Zone | None = None
    condition: str | None = None

    # Escape hatch
    parameters: dict[str, T.Any] = {}


class Category(Enum):
    ACTIVATED = "activated"
    STATIC = "static"
    SPELL = "spell"
    TRIGGERED = "triggered"


class Ability(T.NamedTuple):
    category: Category
    effects: list[Effect] = []
    cost: list[str] = []
    trigger: str | None = None


class Card(T.NamedTuple):
    name: str
    type: CardType
    abilities: list[Ability] = []
    keywords: set[str] = set()
