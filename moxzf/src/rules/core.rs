use crate::card::Card;
use linkme::distributed_slice;
use std::{collections::HashMap, sync::LazyLock};

pub struct Rule {
    pub name: &'static str,
    pub desc: &'static str,
    pub deps: &'static [&'static str],
    pub eval: fn(&Card) -> bool,
}

pub struct RulesEngine {
    rules: HashMap<&'static str, &'static Rule>,
}

impl RulesEngine {
    pub fn init() -> &'static Self {
        static ENGINE: LazyLock<RulesEngine> = LazyLock::new(|| {
            let mut rules = HashMap::new();

            for rule in RULES {
                rules.insert(rule.name, rule);
            }

            RulesEngine { rules }
        });

        &ENGINE
    }

    pub fn eval(&self, card: &Card, rule: &str) -> bool {
        self.rules
            .get(rule)
            .expect(&format!("Non-existent rule {}", rule))
            .eval(card, self)
    }
}

impl Rule {
    fn eval(&self, card: &Card, engine: &RulesEngine) -> bool {
        self.deps.iter().all(|rule| engine.eval(card, rule)) && (self.eval)(card)
    }
}

#[distributed_slice]
pub static RULES: [Rule];

macro_rules! rule {
    (
        name: $name:literal,
        desc: $desc:literal,
        depends_on: [$($dep:literal),*],
        positive: [$($pos:literal),*],
        negative: [$($neg:literal),*],
        rule: |$card:ident| $body:expr
    ) => {
        #[::linkme::distributed_slice(crate::RULES)]
        #[allow(non_upper_case_globals)]
        static ${concat(RULE_, $name)}: crate::Rule =
            crate::Rule {
                name: $name,
                desc: $desc,
                deps: &[$($dep),*],
                eval: |$card| $body,
            };

        #[cfg(test)]
        #[allow(non_snake_case)]
        mod ${concat(rule_, $name, _tests)} {
            #[test]
            fn test_positive_matches() {
                let cards = crate::load_cards();
                let engine = crate::RulesEngine::init();

                $(
                    let card = cards.iter().find(|c| c.name() == $pos).expect(concat!("Card does not exist: ", $pos));
                    assert!(engine.eval(card, $name), concat!("Expected card ", $pos, " to match ", $name));
                )*
            }

            #[test]
            fn test_negative_matches() {
                let cards = crate::load_cards();
                let engine = crate::RulesEngine::init();

                $(
                    let card = cards.iter().find(|c| c.name() == $neg).expect(concat!("Card does not exist: ", $neg));
                    assert!(!engine.eval(card, $name), concat!("Expected card ", $neg, " not to match ", $name));
                )*
            }
        }
    };
}
