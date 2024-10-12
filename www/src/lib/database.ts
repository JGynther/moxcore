import { useState, useEffect, createContext, useContext } from "react";

// FIXME: this should automatically match Python implementation.
type Card = {
    id: number;
    name: string;
    sid: string; // Scryfall ID
    type: string;
    mana: string;
    oracle: string;
    image: string;
    formats: string;
    neighbours: number[];
    flavor?: string;
    power?: string;
    toughness?: string;
};

type Cards = {
    scryfall_base_uri: string;
    scryfall_image_base_uri: string;
    cards: Card[];
};

const useGetCardData = () => {
    const [data, setData] = useState<Cards>();
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadCardData() {
            const result = await fetch("/cards.experimental.json.gz");
            const data: Cards = await result.json();
            setData(data);
            setIsLoading(false);
        }

        loadCardData();
    }, []);

    return { isLoading, data };
};

// @ts-ignore
const Database = createContext<Cards>();
const useDatabase = () => useContext(Database);

export { type Card, type Cards, useGetCardData, Database, useDatabase };
