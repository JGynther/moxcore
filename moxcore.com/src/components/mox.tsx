import { useDatabase } from "@lib/database";

const MoxDiagnostic = ({ id }: { id: number }) => {
    const data = useDatabase();
    const card = data.cards[id];

    return (
        <details className="mox-diagnostic">
            <summary>Compiler diagnostic</summary>
            <pre>{card.meta.moxc_diagnostic}</pre>
        </details>
    );
};

export { MoxDiagnostic };
