import { useState } from "react";
import { NavLink, Link } from "react-router-dom";

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
        <NavLink to={`/cards/${parent}/${slug}`}>
            <div>{card.name}</div>
            <div>
                <MTGText>{card.mana_cost}</MTGText>
            </div>
            <div>{card.type_line}</div>
        </NavLink>
    );
};

const Similar = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const slug = createCardSlug(card);

    type Options = keyof Card["neighbours"];
    const [selected, setSelected] = useState<Options>("moxc");

    return (
        <>
            <div className="similar-cards-list">
                {card.neighbours[selected].map((child_id) => (
                    <CardPreview key={child_id} id={child_id} parent={slug} />
                ))}
            </div>
            <div className="select-similarity-metric">
                <select
                    value={selected}
                    onChange={(event) => setSelected(event.target.value as Options)}
                >
                    {Object.keys(card.neighbours).map((option) => (
                        <option key={option} value={option}>
                            {option}
                        </option>
                    ))}
                </select>
                <abbr title="You can choose between two different similarity metrics.">
                    What is this?
                </abbr>
                <Link to="">Learn how card similarity works ↗</Link>
            </div>
        </>
    );
};

export { Similar };
