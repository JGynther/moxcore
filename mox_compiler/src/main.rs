mod combinators;
mod parsers;

static TEST: &str =
    "Flying (creature with flying....)\nLorem ipsum dolor sit amet.\n{T}, {1}: Lorem ipsum dolor.";

fn main() {
    #[rustfmt::skip]
    let lexer = combinators::many(
        combinators::choice!(
            parsers::reminder(),
            parsers::symbol(),
            parsers::text()
        )
    );

    println!("{:?}", lexer(TEST).expect("Lexed nothing?").0)
}
