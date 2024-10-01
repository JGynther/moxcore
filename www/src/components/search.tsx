import { useState } from "react";
import { Link } from "react-router-dom";

import { useDatabase } from "@lib/database";
import { useOnClickOutside } from "@lib/outside";

import { MTGText } from "@components/mtg";

type AutoCompleteResult = {
    id: number;
    name: string;
    type_line: string;
    mana_cost: string;
}[];

type SuggestionsProps = {
    cards: AutoCompleteResult;
    reset: () => void;
};

const Suggestions = ({ cards, reset }: SuggestionsProps) => {
    const top10 = cards.slice(0, 10);

    return (
        <div className="Autocomplete">
            {top10.map((item) => (
                <Link to={`/cards/${item.id}`} key={item.id} onClick={() => reset()}>
                    {item.name} <MTGText>{item.mana_cost}</MTGText> — {item.type_line}
                </Link>
            ))}

            {cards.length > 10 && <div>+ {cards.length - 10} more...</div>}
        </div>
    );
};

const Search = () => {
    const data = useDatabase();
    const [suggestions, setSuggestions] = useState<AutoCompleteResult>([]);

    const autoComplete = (query: string) => {
        let normalized = query.trim().toLowerCase();
        if (normalized === "") return reset();

        const exact = data.cards.filter((cards) => cards.name.toLowerCase() === normalized);
        const prefix = data.cards.filter((card) => card.name.toLowerCase().startsWith(normalized));
        const substring = data.cards.filter((card) => card.name.toLowerCase().includes(normalized));

        const matches = [...exact, ...prefix, ...substring];
        const uniques = new Set(matches);
        const filtered = Array.from(uniques);

        setSuggestions(
            filtered.map((card) => {
                return {
                    id: card.id,
                    name: card.name,
                    type_line: card.type_line,
                    mana_cost: card.mana_cost,
                };
            })
        );
    };

    const reset = () => setSuggestions([]);
    const ref = useOnClickOutside<HTMLFormElement>(() => reset());

    return (
        <form ref={ref} onSubmit={(event) => event.preventDefault()} className="Search">
            <input
                type="text"
                placeholder='Search e.g. "Black Lotus" or "Chrome Mox"'
                onFocus={(event) => autoComplete(event.target.value)}
                onChange={(event) => autoComplete(event.target.value)}
            />
            <Suggestions cards={suggestions} reset={reset} />
        </form>
    );
};

export default Search;
