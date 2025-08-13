pub mod card;

use anyhow::Result;
use card::ScryfallCardObject;
use reqwest;
use reqwest::header;
use serde::Deserialize;
use serde_json;
use std::fs;
use std::io::Write;

const SCRYFALL_BULK_URL: &str = "https://api.scryfall.com/bulk-data";

fn cache_path() -> std::path::PathBuf {
    match std::env::home_dir() {
        Some(home) => {
            let path = home.join(".cache/scrycache");
            std::fs::create_dir_all(&path).unwrap();
            path.join("scryfall_cards.json")
        }
        None => panic!(),
    }
}

#[derive(Debug, Deserialize)]
struct BulkData {
    #[serde(rename = "type")]
    _type: String,
    download_uri: String,
}

#[derive(Debug, Deserialize)]
struct BulkDataResponse {
    data: Vec<BulkData>,
}

fn make_client() -> reqwest::blocking::Client {
    let mut headers = header::HeaderMap::new();

    headers.insert(
        header::USER_AGENT,
        header::HeaderValue::from_static("moxcore/0.1"),
    );

    headers.insert(
        header::ACCEPT,
        header::HeaderValue::from_static("application/json"),
    );

    reqwest::blocking::Client::builder()
        .default_headers(headers)
        .build()
        .unwrap()
}

fn refresh_cards_cache(path: &std::path::PathBuf) -> Result<()> {
    let client = make_client();

    let response: BulkDataResponse = client
        .get(SCRYFALL_BULK_URL)
        .send()?
        .error_for_status()?
        .json()?;

    let uri = response
        .data
        .into_iter()
        .find(|entry| entry._type == "oracle_cards")
        .map(|entry| entry.download_uri)
        .unwrap();

    println!("Downloading {uri}...");

    let json = client.get(uri).send()?.text()?;

    let mut file = fs::File::create(path)?;
    file.write_all(json.as_bytes())?;

    Ok(())
}

pub fn load_scryfall_cards_with_cache() -> Vec<ScryfallCardObject> {
    let cache = cache_path();

    match cache.exists() {
        true => println!("✔ Found local cache — using it"),
        false => refresh_cards_cache(&cache).unwrap(),
    };

    let data = std::fs::read_to_string(cache).unwrap();
    let cards: Vec<ScryfallCardObject> = serde_json::from_str(&data).unwrap();

    println!("✔ Loaded {} cards", cards.len());

    cards
}

#[test]
fn test_load() {
    load_scryfall_cards_with_cache();
}
