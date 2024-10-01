import { Link } from "react-router-dom";

import { useDatabase } from "@lib/database";
import { MTGText } from "@components/mtg";

type ID = { id: number };

type PreviewProps = {
    id: number;
    parent: number;
};

const CardPreview = ({ id, parent }: PreviewProps) => {
    const data = useDatabase();
    const card = data.cards[id];

    return (
        <Link
            to={`/cards/${parent}/${id}`}
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

    return (
        <div className="similar-cards-list">
            {card.neighbours.map((child_id) => (
                <CardPreview key={child_id} id={child_id} parent={id} />
            ))}
        </div>
    );
};

export { Similar };
