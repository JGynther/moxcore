import { defineConfig } from "@rsbuild/core";
import { pluginReact } from "@rsbuild/plugin-react";
import { pluginSass } from "@rsbuild/plugin-sass";
import { pluginBabel } from "@rsbuild/plugin-babel";

export default defineConfig({
    html: {
        title: "Mirror Mox",
    },
    plugins: [
        pluginReact(),
        pluginSass(),
        pluginBabel({
            include: /\.(?:jsx|tsx)$/,
            babelLoaderOptions(opts) {
                opts.plugins?.unshift("babel-plugin-react-compiler");
            },
        }),
    ],
});
