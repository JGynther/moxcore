import { useState, useEffect, createContext, useContext } from "react";

// FIXME: this should automatically match Python implementation.
type Card = {
    id: number;
    name: string;
    scryfall_id: string;
    type_line: string;
    mana_cost: string;
    color_identity: number[];
    oracle_text: string;
    flavor_text: string;
    set: string;
    collector_number: string;
    image_fragment: string;
    neighbours: number[];
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
            const result = await fetch("/cards.json.gz");
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
