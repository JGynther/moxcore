import { useState } from "react";
import { Link } from "react-router-dom";

import { MTGText } from "@components/mtg";
import { Card, createCardSlug, useDatabase } from "@lib/database";

type ID = { id: number };

type PreviewProps = {
    id: number;
    parent: string;
};

const CardPreview = ({ id, parent }: PreviewProps) => {
    const data = useDatabase();

    const card = data.cards[id];
    const slug = createCardSlug(card);

    return (
        <Link
            to={`/cards/${parent}/${slug}`}
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        >
            <div>{card.name}</div>
            <div>
                <MTGText>{card.mana_cost}</MTGText>
            </div>
            <div>{card.type_line}</div>
            <div>
                <MTGText short>{card.oracle_text}</MTGText>
            </div>
        </Link>
    );
};

const Similar = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const slug = createCardSlug(card);

    type Options = keyof Card["neighbours"];
    const [selected, setSelected] = useState<Options>("hybrid");

    return (
        <>
            <select
                value={selected}
                onChange={(event) => setSelected(event.target.value as Options)}
            >
                <option value="bm25">BM25</option>
                <option value="hybrid">Hybrid</option>
            </select>
            <div className="similar-cards-list">
                {card.neighbours[selected].map((child_id) => (
                    <CardPreview key={child_id} id={child_id} parent={slug} />
                ))}
            </div>
        </>
    );
};

export { Similar };
