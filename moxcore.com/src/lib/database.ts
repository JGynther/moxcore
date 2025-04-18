import { useState, useEffect, createContext, useContext } from "react";

// FIXME: this should automatically match Python implementation.
type Card = {
    id: number;
    scryfall_id: string;
    formats: string;

    name: string;
    type_line: string;
    mana_cost: string;
    oracle_text: string;
    image: string;
    flavor_text: string;
    power?: string;
    toughness?: string;

    neighbours: {
        bm25: number[];
        moxc: number[];
    };
};

type Cards = {
    scryfall_base_uri: string;
    scryfall_image_base_uri: string;
    cards: Card[];
    search: CardSearchArtifact[];
    slugs: Map<string, number>;
};

type CardSearchArtifact = {
    slug: string;
    name: string;
    type_line: string;
    mana_cost: string;
};

const createCardSlug = (card: Card) =>
    card.name.toLowerCase().replaceAll(" ", "-").replaceAll(",", "").replaceAll("'", "");

const constructImageUri = (baseUri: string, image: string, scryfall_id: string, size = "normal") =>
    `${baseUri}/${size}/${image}/${scryfall_id}.jpg`;

const constructScryfallUri = (baseUri: string, scryfall_id: string) => `${baseUri}/${scryfall_id}`;

const useGetCardData = () => {
    const [data, setData] = useState<Cards>();
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadCardData() {
            const result = await fetch("/cards.experimental.json.gz");
            const data: Cards = await result.json();

            const [slugIndex, searchIndex] = createIndex(data.cards);
            data.slugs = slugIndex;
            data.search = searchIndex;

            setData(data);
            setIsLoading(false);
        }

        loadCardData();
    }, []);

    return { isLoading, data };
};

const createIndex = (cards: Card[]): [Map<string, number>, CardSearchArtifact[]] => {
    const slugIndex: Map<string, number> = new Map();
    const searchIndex: CardSearchArtifact[] = [];

    cards.forEach((card) => {
        const slug = createCardSlug(card);
        slugIndex.set(slug, card.id);
        searchIndex.push({
            slug,
            name: card.name,
            type_line: card.type_line,
            mana_cost: card.mana_cost,
        });
    });

    return [slugIndex, searchIndex];
};

// @ts-ignore
const Database = createContext<Cards>();
const useDatabase = () => useContext(Database);

export type { Card, CardSearchArtifact };
export {
    createCardSlug,
    useGetCardData,
    Database,
    useDatabase,
    constructScryfallUri,
    constructImageUri,
};
