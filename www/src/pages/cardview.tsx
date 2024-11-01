import { useParams } from "react-router-dom";

import { useScrollToTop } from "@lib/scroll";
import { useDatabase } from "@lib/database";

import { CardComponent as Card } from "@components/card";
import { Similar } from "@components/similar";

const CardView = () => {
    useScrollToTop();

    const data = useDatabase();
    const { slug } = useParams();

    // FIXME: actually handle errors
    if (!slug) throw new Error();

    const id = data.slugs.get(slug)!;
    const card = data.cards[id];

    return (
        <>
            <Card id={card.id} />
            <Similar id={card.id} />
        </>
    );
};

export default CardView;
