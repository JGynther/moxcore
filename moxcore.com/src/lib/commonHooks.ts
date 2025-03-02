import { createCardSlug, useDatabase } from "@lib/database";

const useRandomCard = () => {
    const data = useDatabase();
    const randomCardId = Math.floor(Math.random() * data.cards.length);
    const randomCardSlug = createCardSlug(data.cards[randomCardId]);
    return `/cards/${randomCardSlug}?random=true`;
};

export { useRandomCard };
