mod normalize;
pub(super) use normalize::Normalize;

use scrycache::card::Color;

#[derive(Debug)]
enum Face {
    Front,
    Back,
}

#[derive(Debug)]
pub struct Card {
    id: String,
    name: String,

    oracle_text: String,
    type_line: String,
    colors: Vec<Color>,
    cmc: f32,
    power: Option<String>,
    toughness: Option<String>,

    face: Option<Face>,
}

macro_rules! is_type {
    ($keyword:ident) => {
        pub fn ${concat(is_, $keyword)}(&self) -> bool {
            self.type_line.contains(stringify!($keyword))
        }
    };
}

macro_rules! is_color {
    ($color:ident) => {
        #[allow(non_snake_case)]
        pub fn ${concat(is_, $color)}(&self) -> bool {
            self.colors.contains(&Color::$color)
        }
    };
}

impl Card {
    // Card types
    is_type!(artifact);
    is_type!(battle);
    is_type!(creature);
    is_type!(enchantment);
    is_type!(instant);
    is_type!(land);
    is_type!(planeswalker);
    is_type!(sorcery);

    // Supertypes
    is_type!(legendary);
    is_type!(basic);
    is_type!(snow);

    // Colors
    is_color!(W);
    is_color!(U);
    is_color!(B);
    is_color!(R);
    is_color!(G);

    pub fn is_multifaced(&self) -> bool {
        self.face.is_some()
    }

    pub fn oracle(&self, text: &str) -> bool {
        self.oracle_text.contains(text)
    }
}
