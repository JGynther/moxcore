import { Link } from "react-router-dom";
import version from "../version.json";
import { useSearchParams } from "react-router-dom";

import Search from "@components/search";
import { GradientButton } from "@components/common";
import { useRandomCard } from "@lib/commonHooks";

const Header = ({ hasSearch = true }) => {
    const [searchParams, _] = useSearchParams();
    const random = searchParams.get("random");
    const randomUri = useRandomCard();

    return (
        <header className="Header">
            <div>
                <Link to="/">
                    <h1>Moxcore</h1>
                </Link>
                <div className="badge">Alpha</div>
            </div>
            {hasSearch && <Search />}
            {random && <GradientButton href={randomUri}>Random Card</GradientButton>}
        </header>
    );
};

const Footer = () => {
    const thisYear = new Date().getFullYear();
    const copyright = thisYear === 2024 ? 2024 : `2024 - ${thisYear}`;

    return (
        <footer className="Footer">
            <p>
                Parts of Moxcore are unofficial Fan Content permited under the Wizards of the
                Coast's Fan Content Policy. Moxcore is not endorsed or sponsored by Wizards of the
                Coast. Portions of the materials used are property of Wizards of the Coast.
                ©Wizards of the Coast LLC.
            </p>
            <p>Everything else © {copyright} Joona Gynther.</p>
            <hr />
            <p>Code is open source and available under a MIT / Apache 2.0 dual license.</p>
            <br />
            <p>
                App version: <i>{version.rev}</i>
            </p>
        </footer>
    );
};

type LayoutProps = { hasSearch?: boolean } & React.PropsWithChildren;
const Layout = ({ hasSearch = false, children }: LayoutProps) => {
    return (
        <>
            <Header hasSearch={hasSearch} />
            <main>{children}</main>
            <Footer />
        </>
    );
};

export default Layout;
