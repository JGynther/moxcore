#![feature(macro_metavar_expr_concat)]

pub mod card;
pub mod rules;

use crate::card::{Card, Normalize};
pub use crate::rules::core::{ENGINE, Rule};

use scrycache::{card::Legality, load_scryfall_cards_with_cache};

pub fn load_cards() -> Vec<Card> {
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
}
