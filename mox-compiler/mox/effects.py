import re
import typing as T

from mox.data_types import Effect, EType, Zone
from mox.target import try_to_figure_out_target


def try_to_parse_effect_type(effect: str) -> tuple[EType, Zone, Zone]:
    etype: EType = EType.UNKNOWN
    source: Zone = Zone.BATTLEFIELD
    destination: Zone = Zone.BATTLEFIELD

    match effect:
        # Exile effects
        case _ if re.search(r"exile.+(?:target|all)", effect):
            etype = EType.EXILE
            destination = Zone.EXILE

        # Destroy effects
        case _ if re.search(r"destroy.+(?:target|all)", effect):
            etype = EType.DESTROY
            destination = Zone.GRAVEYARD

        # Life gain
        case _ if re.search(r"gain.+life", effect):
            etype = EType.LIFE_GAIN

        # Token creation
        case _ if effect.startswith("create") or "token" in effect:
            etype = EType.TOKENS

        # Dealing damage
        case _ if re.search(r"deals?.+damage", effect):
            etype = EType.DAMAGE

        # Drawing cards
        case _ if re.search(r"draw.+cards?", effect):
            etype = EType.DRAW
            source = Zone.LIBRARY
            destination = Zone.HAND

        # Direct prevent effects like "Fog"
        case _ if "prevent" in effect:
            etype = EType.PREVENTION

        # Counterspells
        case _ if re.search(r"counter.+spell", effect):
            etype = EType.PREVENTION
            source = Zone.STACK
            destination = Zone.GRAVEYARD

        # Counters (+1/+1, -1/-1, etc.)
        case _ if re.search(r"counters?\b", effect):
            etype = EType.COUNTERS

        case _ if "add {" in effect:
            etype = EType.MANA

        case _ if "discard" in effect:
            etype = EType.DISCARD
            source = Zone.HAND
            destination = Zone.GRAVEYARD

    return etype, source, destination


def parse_effect(effect: str) -> Effect | None:
    if not (effect := effect.strip()):
        return

    condition = None

    if effect.startswith("if"):
        condition, effect = effect.split(",", 1)

    etype, source, destination = try_to_parse_effect_type(effect)
    target, effect = try_to_figure_out_target(effect)

    parameters: dict[str, T.Any] = {}

    return Effect(
        type=etype,
        text=effect.strip(),
        target=target,
        source=source,
        destination=destination,
        condition=condition,
        parameters=parameters,
    )


def parse_effects(input: str) -> list[Effect]:
    effects = []

    for effect in input.split("."):
        if not effect:
            continue

        effects.append(parse_effect(effect))

    return effects
