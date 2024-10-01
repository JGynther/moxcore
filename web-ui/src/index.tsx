import "@css/index.scss";

import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";

import Layout from "@components/layout";
import Search from "@components/search";

import Home from "@pages/home";
import CardView from "@pages/cardview";
import Compare from "@pages/compare";

import { useGetCardData, Database } from "@lib/database";

const Data = ({ children }: React.PropsWithChildren) => {
    const { isLoading, data } = useGetCardData();
    if (isLoading) return;
    if (!data) throw new Error();
    return <Database.Provider value={data}>{children}</Database.Provider>;
};

const router = createBrowserRouter([
    {
        element: (
            <Data>
                <Layout>
                    <Outlet />
                </Layout>
            </Data>
        ),
        children: [
            { path: "/", element: <Home /> },
            {
                element: (
                    <>
                        <Search />
                        <Outlet />
                    </>
                ),
                children: [
                    { path: "/cards/:id", element: <CardView /> },
                    { path: "/cards/:parent/:child", element: <Compare /> },
                ],
            },
        ],
    },
]);

const rootEl = document.getElementById("root");

if (rootEl) {
    const root = ReactDOM.createRoot(rootEl);
    root.render(
        <React.StrictMode>
            <RouterProvider router={router} />
        </React.StrictMode>
    );
}
