from parsing.combinators import Choice, Many
from parsing.keywords import inject_keywords
from parsing.lexing import Keyword, Reminder, Symbol, Text


def main():
    lexer = Many(
        Choice(
            [
                Symbol(),
                Reminder(),
                Keyword(),
                Text(),
            ]
        )
    )

    TEST = "Flying (creature with flying....)\nLorem ipsum dolor sit amet.\n{T}, {1}: Lorem ipsum dolor."
    TEST2 = "Lorem Ipsum Flying"
    TEST3 = "Flying Lorem (test) Cumulative upkeep"
    TEST5 = "Flying, double strike, lifelink."

    for test in [TEST, TEST2, TEST3, TEST5]:
        input = inject_keywords(test)
        result = lexer(input)
        print(result)


if __name__ == "__main__":
    main()
