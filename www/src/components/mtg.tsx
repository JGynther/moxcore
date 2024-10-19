import { lexer, type Token, TokenType } from "@lib/magic/lexer";

type MTGTextProps = { short?: boolean; children: string };

const MTGText = ({ short = false, children }: MTGTextProps) => {
    const tokens = lexer(children).result;

    const renderToken = (token: Token, index: number) => {
        if (!token) return null;

        switch (token.type) {
            case TokenType.TEXT:
                return token.value;

            case TokenType.KEYWORD:
                if (short) return token.value;
                return (
                    <abbr key={index} title={`KEYWORD: ${token.value.toLocaleUpperCase()}`}>
                        {token.value}
                    </abbr>
                );

            case TokenType.REMINDER:
                if (short) return null;
                return <i key={index}>({token.value})</i>;

            case TokenType.SYMBOL:
                const symbol = token.value.replaceAll("/", "");
                return (
                    <img key={index} src={`https://svgs.scryfall.io/card-symbols/${symbol}.svg`} />
                );

            default:
                return null;
        }
    };

    return <span className="MTG">{tokens.map((token, index) => renderToken(token, index))}</span>;
};

const MTGOracleText = ({ children }: { children: string }) =>
    children.split("\n").map((text, index) => (
        <p key={index}>
            <MTGText>{text}</MTGText>
        </p>
    ));

export { MTGText, MTGOracleText };
