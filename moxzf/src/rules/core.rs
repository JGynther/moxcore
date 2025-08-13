use std::{
    collections::HashMap,
    sync::{LazyLock, RwLock},
};

use crate::card::Card;

pub struct Rule {
    pub name: &'static str,
    pub desc: &'static str,
    pub deps: Vec<&'static str>,
    pub eval: fn(&Card) -> bool,
}

pub struct RulesEngine {
    rules: RwLock<HashMap<&'static str, Rule>>,
}

impl RulesEngine {
    fn new() -> Self {
        Self {
            rules: RwLock::new(HashMap::new()),
        }
    }

    pub fn add_rule(&self, name: &'static str, rule: Rule) {
        self.rules.write().unwrap().insert(name, rule);
    }

    pub fn eval(&self, card: &Card, rule: &str) -> bool {
        self.rules.read().unwrap().get(rule).unwrap().eval(card)
    }
}

pub static ENGINE: LazyLock<RulesEngine> = LazyLock::new(RulesEngine::new);

#[macro_export]
macro_rules! rule {
    (
        name: $name:literal,
        desc: $desc:literal,
        depends_on: [$($dep:literal),*],
        rule: |$card:ident| $body:expr
    ) => {
        ENGINE.add_rule($name,
            Rule {
                name: $name,
                desc: $desc,
                deps: vec![$($dep),*],
                eval: |$card| $body,
            }
        );
    };

    (
        name: $name:literal,
        desc: $desc:literal,
        rule: |$card:ident| $body:expr
    ) => {
        rule!(
            name: $name,
            desc: $desc,
            depends_on: [],
            rule: |$card| $body
        )
    };
}

impl Rule {
    fn eval(&self, card: &Card) -> bool {
        self.deps.iter().all(|rule| ENGINE.eval(card, rule)) && (self.eval)(card)
    }
}
