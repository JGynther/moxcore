import { defineConfig } from "@rsbuild/core";
import { pluginReact } from "@rsbuild/plugin-react";
import { pluginSass } from "@rsbuild/plugin-sass";

export default defineConfig({
    html: {
        title: "Mirror Mox",
    },
    plugins: [pluginReact(), pluginSass()],
});
