import typing as T

type Rest = str
type Result = T.Optional[tuple[T.Any, Rest]]
type Parser = T.Callable[[str], Result]


def Literal(pattern: str) -> Parser:
    length = len(pattern)

    def func(input: str):
        if input.startswith(pattern):
            return pattern, input[length:]

    return func


def Choice(parsers: list[Parser]) -> Parser:
    def func(input: str):
        for parser in parsers:
            if result := parser(input):
                return result

    return func


def Many(parser: Parser) -> Parser:
    def func(input: str):
        rest = input
        results = []

        while result := parser(rest):
            results.append(result[0])
            rest = result[1]

        if not results:
            return None

        return results, rest

    return func


def AndThen(p1: Parser, p2: Parser) -> Parser:
    def func(input: str):
        if result := p1(input):
            if result2 := p2(result[1]):
                return (result[0], result2[0]), result2[1]

    return func


def Map(parser: Parser, map_fn: T.Callable) -> Parser:
    def func(input: str):
        if result := parser(input):
            (value, rest) = result
            return map_fn(value), rest

    return func


def Left(p1: Parser, p2: Parser) -> Parser:
    return Map(AndThen(p1, p2), lambda result: result[0])


def Right(p1: Parser, p2: Parser) -> Parser:
    return Map(AndThen(p1, p2), lambda result: result[1])


def Between(p1: Parser, p2: Parser, p3: Parser) -> Parser:
    return Right(p1, Left(p2, p3))


def NotIn(excluded: str) -> Parser:
    def char(input: str):
        if input and (char := input[0]) not in excluded:
            return (char, input[1:])

    return Map(Many(char), lambda x: "".join(x))


def BetweenChars(start: str, end: str) -> Parser:
    return Between(Literal(start), NotIn(start + end), Literal(end))
