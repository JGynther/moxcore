import { Link } from "react-router-dom";

import { useDatabase } from "@lib/database";
import Search from "@components/search";

const GradientButton = ({ href, children }: { href: string } & React.PropsWithChildren) => (
    <div className="gradient-border">
        <Link to={href}>{children}</Link>
    </div>
);

const Home = () => {
    const data = useDatabase();
    const randomCard = Math.floor(Math.random() * data.cards.length);
    const randomUri = `/cards/${randomCard}`;
    const indexedCards = data.cards.length.toLocaleString("fi-FI");

    return (
        <>
            <div className="Hero">
                <div>
                    <h1>
                        <mark>A similarity search engine for</mark>
                        <br /> Magic: The Gathering
                    </h1>
                    <p>
                        Mirror Mox is currently indexing
                        <mark>
                            <b> {indexedCards} </b>
                        </mark>
                        Magic cards.
                        <br />
                        Let's find your next favorite card! Start by searching below ↓
                    </p>
                    <Search />
                    <div className="Buttons">
                        <GradientButton href={randomUri}>About Mirror Mox</GradientButton>
                        <GradientButton href={randomUri}>How does it work?</GradientButton>
                        <GradientButton href={randomUri}>Random Card</GradientButton>
                    </div>
                </div>
            </div>
            <div className="Info">
                <h2 className="Center-Inline-Image">
                    What is this
                    <img
                        src="/static/madness.png"
                        title='"Madness {B}" ©Wizards of the Coast LLC.'
                    />
                    ?
                </h2>
                <p>test</p>
            </div>
        </>
    );
};

export default Home;
