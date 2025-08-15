rule!(
    name: "creature",
    desc: "All creatures",
    depends_on: [],
    positive: ["colossal dreadmaw", "birds of paradise", "dryad arbor"],
    negative: ["forest", "counterspell"],
    rule: |card| card.is_creature()
);

rule!(
    name: "blue",
    desc: "All blue cards",
    depends_on: [],
    positive: ["counterspell", "anowon, the ruin thief"],
    negative: ["lightning bolt", "abzan guide"],
    rule: |card| card.is_U()
);

rule!(
    name: "legendaryBlueCreature",
    desc: "",
    depends_on: ["creature", "blue"],
    positive: [],
    negative: [],
    rule: |card| card.is_legendary()
);

rule!(
    name: "diesToDoomblade",
    desc: "Non-black creatures",
    depends_on: ["creature"],
    positive: [],
    negative: [],
    rule: |card| !card.is_B()
);

rule!(
    name: "cardDraw",
    desc: "Card draw",
    depends_on: [],
    positive: [],
    negative: [],
    rule: |card| oracle_regex!(card, r"draws?.+cards?")
);
