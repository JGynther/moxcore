import re

TARGET_END_SEQUENCES = r"|\b".join(
    [
        "$",
        "\\.",
        "able",
        "add",
        "and[^\\/]",
        "are",
        "as",
        "becomes",
        "blocks",
        "by",
        "can",
        "can't",
        "chooses?",
        "cost",
        "creates?",
        "discards?",
        "does",
        "doesn't",
        "draws?",
        "during",
        "equal",
        "except",
        "exchange",
        "exiles?",
        "explores?",
        "face",
        "fights?",
        "for",
        "from",
        "gains?",
        "gets?",
        "hand",
        "has",
        "have",
        "in",
        "it",
        "looks?",
        "loses?",
        "maximum",
        "may",
        "mills?",
        "on the",
        "phase",
        "prevent",
        "put",
        "reveals",
        "sacrifices?",
        "scries",
        "search",
        "shuffles?",
        "skips?",
        "then",
        "this",
        "to",
        "unless",
        "until",
        "up",
        "where",
        "would",
        "you",
    ]
)

end_sequence = rf"(?=\b{(TARGET_END_SEQUENCES)})"

# Instances of "target" optionally prefixed by "up to [...]" or "another" statements
direct_target = r"((up to \w+ )|another )?\btarget(?! of\b)"

# Instances of "all" not followed by "combat" or "damage"
all_target = r"\ball(?!\ combat|\ damage)"

# Instances of "any" followed by allowlist literals
any_target = r"\bany (?=creatures|target|other (?!type))"

each_opponent = "each opponent"

# Combined start sequence
start_sequence = rf"({direct_target}|{all_target}|{any_target}|{each_opponent}).*?"

TARGET_PATTERN = re.compile(start_sequence + end_sequence)


def try_to_figure_out_target(effect: str) -> tuple[str | None, str]:
    match TARGET_PATTERN.search(effect):
        case None:
            return None, effect

        case match:
            target = match.group(0).strip().rstrip(",")
            return target, effect.replace(target, "[[target]]")
