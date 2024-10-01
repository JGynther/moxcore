import { Link } from "react-router-dom";

import { useDatabase, type Card } from "@lib/database";
import { MTGText, MTGOracleText } from "@components/mtg";

const constructImageUri = (baseUri: string, card: Card, size = "normal") =>
    `${baseUri}${size}/${card.image_fragment}${card.scryfall_id}.jpg`;

const constructScryfallUri = (baseUri: string, card: Card) =>
    `${baseUri}${card.set}/${card.collector_number}`;

type ID = { id: number };

const CardImage = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const uri = constructImageUri(data.scryfall_image_base_uri, card);

    return (
        <div className="Card-Image">
            <Link to={`/cards/${id}`}>
                <img src={uri} loading="eager" />
            </Link>
        </div>
    );
};

const CardText = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const scryfallUri = constructScryfallUri(data.scryfall_base_uri, card);

    return (
        <div className="Card-Info">
            <h1>
                {card.name} <MTGText>{card.mana_cost}</MTGText>
            </h1>

            <p>{card.type_line}</p>

            <hr />

            <MTGOracleText>{card.oracle_text}</MTGOracleText>

            <hr />

            {card.flavor_text && (
                <p>
                    <i>{card.flavor_text}</i>
                </p>
            )}

            <a href={scryfallUri} target="_blank" rel="noreferrer">
                Open in Scryfall ↗
            </a>
        </div>
    );
};

const FORMATS = ["Standard", "Pioneer", "Modern", "Legacy", "Pauper", "Vintage", "Commander"];

const RandomLegality = () => {
    switch (Math.floor(Math.random() * 4)) {
        case 0:
            return <div className="legal">Legal</div>;
        case 1:
            return <div className="not-legal">Not legal</div>;
        case 2:
            return <div className="banned">Banned</div>;
        case 3:
            return <div className="restricted">Restricted</div>;
    }
};

const LegalityTable = () => {
    return (
        <div className="card-legality-table">
            {FORMATS.sort().map((format, index) => (
                <div key={index}>
                    <div>{format}</div>
                    <RandomLegality />
                </div>
            ))}
        </div>
    );
};

const CardComponent = ({ id }: ID) => {
    return (
        <div className="Card">
            <CardImage id={id} />
            <CardText id={id} />
            <LegalityTable />
        </div>
    );
};

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

export { CardImage, CardText, CardComponent, Similar, constructScryfallUri };
export type { Card };
