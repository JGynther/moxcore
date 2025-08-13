use moxzf::{ENGINE, Rule, load_cards, rule};

// Just testing
fn main() {
    let cards = load_cards();

    rule!(
        name: "creature",
        desc: "All creatures",
        rule: |card| card.is_creature()
    );

    rule!(
        name: "blue",
        desc: "All blue cards",
        rule: |card| card.is_U()
    );

    rule!(
        name: "legendary-blue-creature",
        desc: "",
        depends_on: ["creature", "blue"],
        rule: |card| card.is_legendary()
    );

    rule!(
        name: "trigger-whenever",
        desc: "",
        rule: |card| card.oracle("whenever")
    );

    rule!(
        name: "search",
        desc: "",
        rule: |card| card.oracle("search")
    );

    rule!(
        name: "dies-to-doomblade",
        desc: "Non-black creatures",
        depends_on: ["creature"],
        rule: |card| !card.is_B()
    );

    let rand_card = cards.get(3675).unwrap();
    dbg!(rand_card);

    dbg!(ENGINE.eval(rand_card, "legendary-blue-creature"));
    dbg!(ENGINE.eval(rand_card, "trigger-whenever"));
    dbg!(ENGINE.eval(rand_card, "search"));
    dbg!(ENGINE.eval(rand_card, "dies-to-doomblade"));
}
