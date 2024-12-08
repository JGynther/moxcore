pub type IResult<'a, Value> = Option<(Value, &'a str)>;

macro_rules! parser {
    ($return_type:ty) => {
        impl Fn(&str) -> IResult<$return_type>
    };
}

pub(crate) use parser;

pub fn literal<'a>(pattern: &'static str) -> parser!(&'a str) {
    move |input| {
        input
            .starts_with(pattern)
            .then(|| (pattern, &input[pattern.len()..]))
    }
}

pub fn many<T>(parser: parser!(T)) -> parser!(Vec<T>) {
    move |input| {
        let mut current = input;
        let mut result = Vec::new();

        while let Some((item, next)) = parser(current) {
            current = next;
            result.push(item);
        }

        if result.is_empty() {
            return None;
        }

        Some((result, current))
    }
}

pub fn predicate<T, F>(parser: parser!(T), predicate: F) -> parser!(T)
where
    F: Fn(&T) -> bool,
{
    move |input| {
        if let Some((item, next)) = parser(input) {
            if predicate(&item) {
                return Some((item, next));
            }
        }
        None
    }
}

pub fn any_character(input: &str) -> IResult<char> {
    match input.chars().next() {
        Some(next) => Some((next, &input[next.len_utf8()..])),
        _ => None,
    }
}

pub fn map<F, A, B>(parser: parser!(A), map_fn: F) -> parser!(B)
where
    F: Fn(A) -> B,
{
    move |input| parser(input).map(|(value, next)| (map_fn(value), next))
}

pub fn pair<A, B>(p1: parser!(A), p2: parser!(B)) -> parser!((A, B)) {
    move |input| {
        p1(input).and_then(|(value, next)| p2(next).map(|(value2, last)| ((value, value2), last)))
    }
}

pub fn left<A, B>(p1: parser!(A), p2: parser!(B)) -> parser!(A) {
    map(pair(p1, p2), |(left, _)| left)
}

pub fn right<A, B>(p1: parser!(A), p2: parser!(B)) -> parser!(B) {
    map(pair(p1, p2), |(_, right)| right)
}

// FIXME
//pub fn choice<T>(parsers: Vec<parser!(T)>) -> parser!(T) {
//    move |input| parsers.iter().find_map(|f| f(input))
//}

// FIXME
// Choice is implemented as a macro for now.
// I can't figure out how to make a choice function that accepts different parsers.
// Regardless of the container (vec, array) I tried I keep running into the fact that
// different `impl Trait`s are different opaque types and the compiler yells at me
// even though the signature of the functions is identical
macro_rules! choice {
    ($($parser:expr),+ $(,)?) => {
        move |input| {
            $(
                if let some_result @ Some(_) = $parser(input) {
                    return some_result;
                }
            )+
            None
        }
    };
}

pub(crate) use choice;
