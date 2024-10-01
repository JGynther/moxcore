import { useParams } from "react-router-dom";

import { useScrollToTop } from "@lib/scroll";
import { useDatabase } from "@lib/database";

import { CardComponent as Card, Similar } from "@components/card";

const CardView = () => {
    useScrollToTop();

    const data = useDatabase();
    const { id } = useParams();

    // FIXME: actually handle errors
    if (!id) throw new Error();
    const card = data.cards[Number(id)];

    return (
        <>
            <Card id={card.id} />
            <Similar id={card.id} />
        </>
    );
};

export default CardView;
