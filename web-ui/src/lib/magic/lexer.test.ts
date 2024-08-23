import { expect, test } from "bun:test";
import { lexer, TokenType } from "@lib/magic/lexer";

const TEST1 = `Flying (creature with flying....)
Lorem ipsum dolor sit amet.
{T}, {1}: Lorem ipsum dolor.`;

const EXPECTED1 = [
    { type: TokenType.KEYWORD, value: "Flying" },
    { type: TokenType.TEXT, value: " " },
    { type: TokenType.REMINDER, value: "creature with flying...." },
    { type: TokenType.TEXT, value: "\nLorem ipsum dolor sit amet.\n" },
    { type: TokenType.SYMBOL, value: "T" },
    { type: TokenType.TEXT, value: ", " },
    { type: TokenType.SYMBOL, value: "1" },
    { type: TokenType.TEXT, value: ": Lorem ipsum dolor." },
];

const TEST2 = "Lorem Ipsum Flying";

const EXPECTED2 = [
    { type: TokenType.TEXT, value: "Lorem Ipsum " },
    { type: TokenType.KEYWORD, value: "Flying" },
];

const TEST3 = "Flying Lorem (test) Cumulative upkeep";

const EXPECTED3 = [
    { type: TokenType.KEYWORD, value: "Flying" },
    { type: TokenType.TEXT, value: " Lorem " },
    { type: TokenType.REMINDER, value: "test" },
    { type: TokenType.TEXT, value: " " },
    { type: TokenType.KEYWORD, value: "Cumulative upkeep" },
];

const TEST4 = "Lorem ipsum dolor sit amet\nLorem ipsum dolor sit amet";

const EXPECTED4 = [{ type: TokenType.TEXT, value: TEST4 }];

const TEST5 = "Flying, double strike, lifelink";
const EXPECTED5 = [
    { type: TokenType.KEYWORD, value: "Flying" },
    { type: TokenType.TEXT, value: ", " },
    { type: TokenType.KEYWORD, value: "double strike" },
    { type: TokenType.TEXT, value: ", " },
    { type: TokenType.KEYWORD, value: "lifelink" },
];

test("Lexer, Base.", () => {
    const lexed = lexer(TEST1);
    expect(lexed.result).toEqual(EXPECTED1);
});

test("Lexer, Keyword at end.", () => {
    const lexed = lexer(TEST2);
    expect(lexed.result).toEqual(EXPECTED2);
});

test("Lexer, Double Keyword including significant whitespace.", () => {
    const lexed = lexer(TEST3);
    expect(lexed.result).toEqual(EXPECTED3);
});

test("Lexer, Only text.", () => {
    const lexed = lexer(TEST4);
    expect(lexed.result).toEqual(EXPECTED4);
});

test("Lexer, Keyword list.", () => {
    const lexed = lexer(TEST5);
    expect(lexed.result).toEqual(EXPECTED5);
});
