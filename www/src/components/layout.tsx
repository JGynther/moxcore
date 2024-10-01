import { Link } from "react-router-dom";
import version from "../version.json";

const Header = () => {
    return (
        <header className="Header">
            <Link to="/">
                <h1>Mirror Mox</h1>
            </Link>
            <div className="badge">Alpha</div>
        </header>
    );
};

const Footer = () => {
    const thisYear = new Date().getFullYear();
    const copyright = thisYear === 2024 ? 2024 : `2024 - ${thisYear}`;

    return (
        <footer className="Footer">
            <p>
                Parts of Mirror Mox are unofficial Fan Content permited under the Wizards of the
                Coast's Fan Content Policy. Mirror Mox is not endorsed or sponsored by Wizards of
                the Coast. Portions of the materials used are property of Wizards of the Coast.
                ©Wizards of the Coast LLC.
            </p>
            <p>Everything else © {copyright} Joona Gynther.</p>
            <hr />
            <p>Code is open source and available under a MIT / Apache 2.0 dual license.</p>
            <br />
            <p>
                Version: <i>{version.rev}</i>
            </p>
        </footer>
    );
};

const Layout = ({ children }: React.PropsWithChildren) => {
    return (
        <>
            <Header />
            <main>{children}</main>
            <Footer />
        </>
    );
};

export default Layout;
