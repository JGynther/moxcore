use moxzf::{RulesEngine, load_cards};

// Just testing
fn main() {
    let cards = load_cards();
    let engine = RulesEngine::init();

    dbg!(
        cards
            .iter()
            .filter(|card| engine.eval(card, "legendaryBlueCreature"))
            .collect::<Vec<_>>()
            .len()
    );
}
