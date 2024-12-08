use crate::combinators::*;

#[derive(Debug)]
pub enum Token {
    Symbol(String),
    Reminder(String),
    Text(String),
}

pub fn symbol() -> parser!(Token) {
    let _symbol = right(
        literal("{"),
        left(
            many(predicate(any_character, |c| match c {
                '{' | '(' | ')' => panic!("Malformed input: unclosed symbol."),
                '}' => false,
                _ => true,
            })),
            literal("}"),
        ),
    );

    map(_symbol, |value| Token::Symbol(String::from_iter(value)))
}

pub fn reminder() -> parser!(Token) {
    let _reminder = right(
        literal("("),
        left(
            many(predicate(any_character, |c| match c {
                '(' => panic!("Malformed input: unclosed reminder."),
                ')' => false,
                _ => true,
            })),
            literal(")"),
        ),
    );

    map(_reminder, |value| Token::Reminder(String::from_iter(value)))
}

pub fn text() -> parser!(Token) {
    let content = many(predicate(any_character, |c| match c {
        '{' | '(' => false,
        '}' | ')' => panic!("Malformed input: unopened tag."),
        _ => true,
    }));

    map(content, |value| Token::Text(String::from_iter(value)))
}
