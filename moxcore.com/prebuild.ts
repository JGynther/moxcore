import { $ } from "bun";

const rev = (await $`git rev-parse HEAD`.text()).slice(0, 7);

const version = {
    rev,
};

const bytes = await Bun.write("./src/version.json", JSON.stringify(version));

console.log(`Current rev: ${rev}`);
console.log(`Wrote ${bytes} bytes`);
