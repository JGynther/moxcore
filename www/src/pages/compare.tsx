import { useParams, Link } from "react-router-dom";

import { MTGText, MTGOracleText } from "@components/mtg";
import { CardImage, type Card, constructScryfallUri } from "@components/card";
import { Similar } from "@components/similar";

import { useDatabase } from "@lib/database";

const CompareTable = ({ parent, child }: { parent: number; child: number }) => {
    const data = useDatabase();

    const parentCard = data.cards[parent];
    const childCard = data.cards[child];

    type RenderFunc = (card: Card) => React.ReactNode;

    const renderFunctions: RenderFunc[] = [
        (card) => (
            <h1>
                {card.name} <MTGText>{card.mana}</MTGText>
            </h1>
        ),
        (card) => <p>{card.type}</p>,
        (card) => <MTGOracleText>{card.oracle}</MTGOracleText>,
        (card) =>
            card.flavor && (
                <p>
                    <i>{card.flavor}</i>
                </p>
            ),
        (card) => {
            const scryfallUri = constructScryfallUri(data.scryfall_base_uri, card);
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

const CompareImages = ({ parent, child }: { parent: number; child: number }) => {
    return (
        <div className="stacked-card-images">
            <CardImage id={parent} />
            <CardImage id={child} />
            <Link to={`/cards/${child}/${parent}`}>Swap ⇆</Link>
        </div>
    );
};

const Compare = () => {
    const { parent, child } = useParams();

    const parentId = Number(parent);
    const childId = Number(child);

    return (
        <>
            <div className="Compare">
                <CompareImages parent={parentId} child={childId} />
                <CompareTable parent={parentId} child={childId} />
            </div>
            <Similar id={parentId} />
        </>
    );
};

export default Compare;
