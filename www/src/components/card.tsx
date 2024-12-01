import { Link } from "react-router-dom";

import { MTGOracleText, MTGText } from "@components/mtg";
import { Similar } from "@components/similar";
import {
    constructImageUri,
    constructScryfallUri,
    createCardSlug,
    useDatabase,
    type Card,
} from "@lib/database";

type ID = { id: number };

const CardImage = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const uri = constructImageUri(data.scryfall_image_base_uri, card.image, card.scryfall_id);

    const slug = createCardSlug(card);

    return (
        <div className="card-image">
            <Link to={`/cards/${slug}`}>
                <img src={uri} loading="eager" />
            </Link>
        </div>
    );
};

const CardText = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];

    const scryfallUri = constructScryfallUri(data.scryfall_base_uri, card.scryfall_id);

    return (
        <div className="card-info">
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

const FORMATS = ["commander", "legacy", "modern", "pauper", "pioneer", "standard", "vintage"];

const Legality = ({ index }: { index: string }) => {
    switch (index) {
        case "0":
            return <div className="not-legal">Not legal</div>;
        case "1":
            return <div className="legal">Legal</div>;
        case "2":
            return <div className="banned">Banned</div>;
        case "3":
            return <div className="restricted">Restricted</div>;
    }
};

const LegalityTable = ({ id }: ID) => {
    const data = useDatabase();
    const card = data.cards[id];
    const formats = card.formats.split("");

    return (
        <div className="card-legality-table">
            {FORMATS.sort().map((format, index) => (
                <div key={index}>
                    <div>{format.charAt(0).toUpperCase() + format.slice(1)}</div>
                    <Legality index={formats[index]} />
                </div>
            ))}
        </div>
    );
};

type CardProps =
    | { id: number; compareTo?: undefined; swap?: undefined }
    | { id: number; compareTo: number; swap: string };

const CardComponent = ({ id, compareTo, swap }: CardProps) => {
    return (
        <div className="card">
            <div>
                <div className="stacked-card-images-test">
                    <CardImage id={id} />
                    {compareTo && (
                        <>
                            <CardImage id={compareTo} />
                            <Link to={swap}>Swap ⇆</Link>
                        </>
                    )}
                </div>
            </div>
            <div>
                <div className="card-info-box">
                    <CardText id={id} />
                    <LegalityTable id={id} />
                </div>
                <Similar id={id} />
            </div>
        </div>
    );
};

export { CardComponent };
