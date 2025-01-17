import typing as T
from dataclasses import dataclass
from functools import partial

from parsing.combinators import BetweenChars, Map, NotIn, Parser
from parsing.keywords import END_KW, START_KW


@dataclass
class Token:
    type: T.Literal["Symbol", "Reminder", "AmbiguousText", "Keyword"]
    value: str

    def __repr__(self):
        return f"{self.type}({self.value.replace('\n', ' ')})"


def Text() -> Parser:
    INVALID = "(){}" + START_KW + END_KW

    return Map(
        NotIn(INVALID),
        partial(Token, "AmbiguousText"),
    )


def Symbol() -> Parser:
    return Map(
        BetweenChars("{", "}"),
        partial(Token, "Symbol"),
    )


def Reminder() -> Parser:
    return Map(
        BetweenChars("(", ")"),
        partial(Token, "Reminder"),
    )


def Keyword() -> Parser:
    return Map(
        BetweenChars(START_KW, END_KW),
        partial(Token, "Keyword"),
    )
