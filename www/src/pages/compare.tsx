import { useParams, Link } from "react-router-dom";

import { MTGText, MTGOracleText } from "@components/mtg";
import { CardImage, constructScryfallUri } from "@components/card";
import { Similar } from "@components/similar";

import { useDatabase, type Card } from "@lib/database";

const CompareTable = ({ parent, child }: { parent: number; child: number }) => {
    const data = useDatabase();

    const parentCard = data.cards[parent];
    const childCard = data.cards[child];

    type RenderFunc = (card: Card) => React.ReactNode;

    const renderFunctions: RenderFunc[] = [
        (card) => (
            <h1>
                {card.name} <MTGText>{card.mana_cost}</MTGText>
            </h1>
        ),
        (card) => <p>{card.type_line}</p>,
        (card) => <MTGOracleText>{card.oracle_text}</MTGOracleText>,
        (card) =>
            card.flavor_text && (
                <p>
                    <i>{card.flavor_text}</i>
                </p>
            ),
        (card) => {
            const scryfallUri = constructScryfallUri(data.scryfall_base_uri, card.scryfall_id);
            return (
                <p>
                    <a href={scryfallUri} target="_blank" rel="noreferrer">
                        Scryfall ↗
                    </a>
                </p>
            );
        },
    ];

    return (
        <div className="Compare-Table">
            {renderFunctions.map((render, index) => {
                const firstContent = render(parentCard);
                const secondContent = render(childCard);

                if (!firstContent && !secondContent) return null;

                return (
                    <div key={index}>
                        <div>{firstContent}</div>
                        <div>{secondContent}</div>
                    </div>
                );
            })}
        </div>
    );
};

const CompareImages = ({ parent, child, url }: { parent: number; child: number; url: string }) => {
    return (
        <div className="stacked-card-images">
            <CardImage id={parent} />
            <CardImage id={child} />
            <Link to={url}>Swap ⇆</Link>
        </div>
    );
};

const Compare = () => {
    const data = useDatabase();
    const { parent, child } = useParams();

    if (!parent || !child) throw new Error("Parent or child param not provided.");

    const parentId = data.slugs.get(parent);
    const childId = data.slugs.get(child);

    if (parentId === undefined || childId === undefined)
        throw new Error("Card slug does not match any card ID.");

    const swapUrl = `/cards/${child}/${parent}`;

    return (
        <>
            <div className="Compare">
                <CompareImages parent={parentId} child={childId} url={swapUrl} />
                <CompareTable parent={parentId} child={childId} />
            </div>
            <Similar id={parentId} />
        </>
    );
};

export default Compare;
