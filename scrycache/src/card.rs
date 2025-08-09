use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(rename_all = "UPPERCASE")]
pub enum Color {
    W,
    U,
    B,
    R,
    G,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Rarity {
    Common,
    Uncommon,
    Rare,
    Special,
    Mythic,
    Bonus,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Games {
    Paper,
    Arena,
    Mtgo,
    Sega,   // What the fuck is this?
    Astral, // What the fuck is this?
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Legality {
    Legal,
    #[serde(rename = "not_legal")]
    NotLegal,
    Restricted,
    Banned,
}

#[derive(Debug, Deserialize)]
pub struct ScryfallLegalities {
    pub alchemy: Legality,
    pub brawl: Legality,
    pub commander: Legality,
    pub duel: Legality,
    pub future: Legality,
    pub gladiator: Legality,
    pub historic: Legality,
    pub legacy: Legality,
    pub modern: Legality,
    pub oathbreaker: Legality,
    pub oldschool: Legality,
    pub pauper: Legality,
    pub paupercommander: Legality,
    pub penny: Legality,
    pub pioneer: Legality,
    pub predh: Legality,
    pub premodern: Legality,
    pub standard: Legality,
    pub standardbrawl: Legality,
    pub timeless: Legality,
    pub vintage: Legality,
}

#[derive(Debug, Deserialize)]
pub struct ScryfallImageURIs {
    pub normal: String,
}

#[derive(Debug, Deserialize)]
pub struct ScryfallCardFace {
    pub cmc: Option<f32>,
    pub colors: Option<Vec<Color>>,
    pub image_uris: Option<ScryfallImageURIs>,
    pub loyalty: Option<String>,
    pub mana_cost: Option<String>,
    pub name: String,
    pub oracle_text: Option<String>,
    pub power: Option<String>,
    pub toughness: Option<String>,
    pub type_line: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct ScryfallCardObject {
    pub card_faces: Option<Vec<ScryfallCardFace>>,
    pub cmc: Option<f32>,
    pub colors: Option<Vec<Color>>,
    pub edhrec_rank: Option<usize>,
    pub game_changer: bool,
    pub games: Vec<Games>,
    pub image_uris: Option<ScryfallImageURIs>,
    pub keywords: Vec<String>,
    pub legalities: ScryfallLegalities,
    pub loyalty: Option<String>,
    pub mana_cost: Option<String>,
    pub name: String,
    pub oracle_text: Option<String>,
    pub power: Option<String>,
    pub rarity: Rarity,
    pub scryfall_uri: String,
    pub set: String,
    pub toughness: Option<String>,
    pub type_line: Option<String>,
}
