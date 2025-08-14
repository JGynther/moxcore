use moxzf::{dbg_eval_rule, load_cards, oracle_regex, rule};

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

    rule!(
        name: "card-draw",
        desc: "Card draw",
        depends_on: [],
        rule: |card| oracle_regex!(card, r"draws?.+cards?")
    );

    let rand_card = cards.get(3675).unwrap();
    dbg!(rand_card);

    dbg!(dbg_eval_rule!(rand_card, "legendary-blue-creature"));
    dbg!(dbg_eval_rule!(rand_card, "trigger-whenever"));
    dbg!(dbg_eval_rule!(rand_card, "search"));
    dbg!(dbg_eval_rule!(rand_card, "dies-to-doomblade"));
    dbg!(dbg_eval_rule!(rand_card, "card-draw"));

    dbg!(
        cards
            .iter()
            .filter(|card| dbg_eval_rule!(card, "legendary-blue-creature"))
            .collect::<Vec<_>>()
            .len()
    );
}
