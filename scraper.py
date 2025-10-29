import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://onepunchmanscan.com"
DATA_PATH = "data/onepunchman.json"

def scrape_chapters():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    chapters = []
    for a in soup.select("a.chapitre"):  # Sélecteur basé sur la structure du site
        url = a["href"]
        title = a.text.strip()
        chapter = {
            "title": title,
            "url": url,
            "pages": scrape_pages(url)
        }
        chapters.append(chapter)

    return chapters

def scrape_pages(chapter_url):
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    pages = []

    for img in soup.select("img[src*='uploads']"):
        pages.append(img["src"])

    return pages

def load_json():
    if not os.path.exists(DATA_PATH):
        return {"name": "One Punch Man", "lang": "fr", "chapters": []}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    data = load_json()
    data["chapters"] = scrape_chapters()
    save_json(data)

if __name__ == "__main__":
    main()
