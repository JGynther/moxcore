use super::{Card, Face};
use scrycache::card::ScryfallCardObject;

fn normalize_oracle(name: &str, oracle_text: Option<String>) -> String {
    oracle_text
        .unwrap_or(String::new())
        .to_lowercase()
        .replace(name, "<|001|>")
        .replace(name.split(",").next().unwrap(), "<|002|>")
}

pub(crate) trait Normalize {
    fn normalize(self) -> Vec<Card>;
}

impl Normalize for ScryfallCardObject {
    fn normalize(self) -> Vec<Card> {
        match self.card_faces {
            None => {
                let name = self.name.to_lowercase();
                let oracle_text = normalize_oracle(&name, self.oracle_text);
                let type_line = self.type_line.unwrap_or(String::new()).to_lowercase();

                vec![Card {
                    id: self.id,
                    name,
                    oracle_text,
                    type_line,
                    colors: self.colors.unwrap_or(Vec::new()),
                    cmc: self.cmc.unwrap_or(0.0),
                    power: self.power,
                    toughness: self.toughness,
                    face: None,
                }]
            }

            Some(card_faces) => card_faces
                .into_iter()
                .enumerate()
                .map(|(i, face)| {
                    let name = face.name.to_lowercase();
                    let oracle_text = normalize_oracle(&name, face.oracle_text);
                    let type_line = face.type_line.unwrap_or(String::new()).to_lowercase();

                    Card {
                        id: self.id.clone(),
                        name,
                        oracle_text,
                        type_line,
                        colors: face.colors.or(self.colors.clone()).unwrap_or(Vec::new()),
                        cmc: face.cmc.or(self.cmc).unwrap_or(0.0),
                        power: face.power,
                        toughness: face.toughness,
                        face: Some(match i {
                            0 => Face::Front,
                            _ => Face::Back,
                        }),
                    }
                })
                .collect(),
        }
    }
}
