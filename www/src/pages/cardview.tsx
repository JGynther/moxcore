import { useParams } from "react-router-dom";

import { useScrollToTop } from "@lib/scroll";
import { useDatabase } from "@lib/database";

import { CardComponent as Card } from "@components/card";

const SingleCard = () => {
    useScrollToTop();

    const data = useDatabase();
    const { slug } = useParams();

    // FIXME: actually handle errors
    if (!slug) throw new Error();

    const id = data.slugs.get(slug)!;
    const card = data.cards[id];

    return <Card id={card.id} />;
};

const TwoCards = () => {
    const data = useDatabase();
    const { parent, child } = useParams();

    if (!parent || !child) throw new Error("Parent or child param not provided.");

    const parentId = data.slugs.get(parent);
    const childId = data.slugs.get(child);

    if (parentId === undefined || childId === undefined)
        throw new Error("Card slug does not match any card ID.");

    const swapUrl = `/cards/${child}/${parent}`;

    return <Card id={parentId} compareTo={childId} swap={swapUrl} />;
};

export { SingleCard, TwoCards };
