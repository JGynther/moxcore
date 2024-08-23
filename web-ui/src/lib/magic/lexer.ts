import { KEYWORDS, MULTIWORD_PREFIX } from "@lib/magic/keyword";

enum TokenType {
    TEXT,
    SYMBOL,
    REMINDER,
    KEYWORD,
    ERROR,
}

type Token = { type: TokenType; value: string };

const TOKENS: Record<string, TokenType> = {
    "{": TokenType.SYMBOL,
    "(": TokenType.REMINDER,
    "}": TokenType.ERROR,
    ")": TokenType.ERROR,
};

type State = { input: string; result: Token[]; pos: number };

const EOF = (state: State): boolean => state.pos >= state.input.length;

const next = (state: State): [string, State] => [
    state.input[state.pos],
    { ...state, pos: state.pos + 1 },
];

const addToken = (type: TokenType, value: string, state: State) =>
    state.result.push({ type, value });

type Lexer = (state: State, ...args: string[]) => State;

const lexText: Lexer = (state: State, text = "") => {
    if (EOF(state)) {
        text && addToken(TokenType.TEXT, text, state);
        return state;
    }

    const [character, newState] = next(state);
    const token = TOKENS[character];

    if (token) {
        text && addToken(TokenType.TEXT, text, state);
        return TOKEN_TO_LEXER[token](newState);
    }

    text += character;

    return lexText(newState, text);
};

const lexSymbol: Lexer = (state) => {
    let c: string;
    let newState = state;
    let symbol = "";

    for (;;) {
        if (EOF(newState)) break;

        [c, newState] = next(newState);

        if (c === "{") continue;
        if (c === "}") break;

        symbol += c;
    }

    addToken(TokenType.SYMBOL, symbol, newState);

    return newState;
};

const lexReminder: Lexer = (state) => {
    let c: string;
    let newState = state;
    let reminder = "";

    for (;;) {
        if (EOF(newState)) break;

        [c, newState] = next(newState);

        if (c === "(") continue;
        if (c === ")") break;

        reminder += c;
    }

    addToken(TokenType.REMINDER, reminder, newState);

    return newState;
};

const lexVoid: Lexer = (_) => _;

const TOKEN_TO_LEXER: Record<TokenType, Lexer> = {
    [TokenType.SYMBOL]: lexSymbol,
    [TokenType.REMINDER]: lexReminder,
    [TokenType.TEXT]: lexText,
    [TokenType.KEYWORD]: lexVoid,
    [TokenType.ERROR]: (_) => {
        // This should mean input is malformed and unprocessable
        throw new Error("Impossible lexer state.");
    },
};

const lexToken: Lexer = (state) => {
    const character = state.input[state.pos];
    return (TOKEN_TO_LEXER[TOKENS[character]] || lexText)(state);
};

const noNeedToFlush = (character: string) => {
    switch (character) {
        case " ":
        case "\n":
        case ",":
            return false;
        default:
            return true;
    }
};

const lexKeywords: Lexer = (state) => {
    const tokens = state.result;
    const newState: State = { ...state, result: [] };

    for (const token of tokens) {
        if (token.type !== TokenType.TEXT) {
            newState.result.push(token);
            continue;
        }

        const current: Token[] = [];

        let buffer = "";
        let store = "";

        // Hacky. To avoid defining same functionality outside of loop
        // Forces flush check at end of text
        token.value += " ";

        for (const character of token.value) {
            if (noNeedToFlush(character)) {
                buffer += character;
                continue;
            }

            const temp = buffer.charAt(0).toUpperCase() + buffer.slice(1);

            if (temp in MULTIWORD_PREFIX) {
                buffer += character;
                continue;
            }

            if (temp in KEYWORDS) {
                store && current.push({ type: TokenType.TEXT, value: store });
                current.push({ type: TokenType.KEYWORD, value: buffer });

                buffer = "";
                store = character;

                continue;
            }

            store += buffer + character;
            buffer = "";
        }

        // To handle the extra whitespace added to force flush
        const remainder = store.slice(0, -1);

        if (remainder) {
            current.push({ type: TokenType.TEXT, value: remainder });
        }

        newState.result.push(...current);
    }

    return newState;
};

const lex: Lexer = (state) => {
    if (EOF(state)) return lexKeywords(state);
    const newState = lexToken(state);
    return lex(newState);
};

const lexer = (input: string) => lex({ input, result: [], pos: 0 });

export { lexer, type Token, TokenType };
