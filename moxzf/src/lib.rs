#![feature(macro_metavar_expr_concat)]

#[macro_use]
pub mod card;
pub mod rules;

use crate::card::{Card, Normalize};
pub use crate::rules::core::{RULES, Rule, RulesEngine};

use scrycache::{card::Legality, load_scryfall_cards_with_cache};
use std::sync::LazyLock;

pub fn load_cards() -> &'static [Card] {
    static CACHE: LazyLock<Vec<Card>> = LazyLock::new(|| {
        load_scryfall_cards_with_cache()
            .into_iter()
            .filter(|card| {
                matches!(
                    card.legalities.vintage,
                    Legality::Legal | Legality::Restricted
                )
            })
            .flat_map(|c| c.normalize())
            .collect()
    });

    &CACHE
}
