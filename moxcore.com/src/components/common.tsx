import { Link } from "react-router-dom";

const GradientButton = ({ href, children }: { href: string } & React.PropsWithChildren) => (
    <div className="gradient-border">
        <Link to={href}>{children}</Link>
    </div>
);

export { GradientButton };
