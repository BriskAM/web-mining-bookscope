"""Web scraper for books.toscrape.com (listing pages)."""
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://books.toscrape.com/catalogue/"
START = BASE + "page-1.html"
HEADERS = {"User-Agent": "BookScope-student-project/1.0"}
RATING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url, session, retries=3):
    for i in range(retries):
        try:
            r = session.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            r.encoding = "utf-8"
            return BeautifulSoup(r.text, "lxml")
        except requests.RequestException:
            time.sleep(1 + i)
    raise RuntimeError(f"failed to fetch {url}")


def parse_listing(soup):
    books = []
    for art in soup.select("article.product_pod"):
        a = art.h3.a
        books.append({
            "title": a["title"],
            "url": urljoin(BASE, a["href"]),
            "price": art.select_one(".price_color").text,
            "rating": RATING[art.select_one("p.star-rating")["class"][1]],
            "in_stock": "In stock" in art.select_one(".availability").text,
        })
    return books


def scrape_listings(delay=0.2):
    session, url, out = requests.Session(), START, []
    while url:
        soup = get_soup(url, session)
        out += parse_listing(soup)
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(delay)
    return out


def parse_detail(url):
    """Fetch one book page: category, description, UPC, review count."""
    soup = get_soup(url, requests.Session())
    crumbs = soup.select("ul.breadcrumb li a")
    desc = soup.select_one("#product_description")
    table = {r.th.text: r.td.text for r in soup.select("table.table-striped tr")}
    return {
        "url": url,
        "category": crumbs[-1].text.strip() if crumbs else None,
        "description": desc.find_next_sibling("p").text.strip() if desc else "",
        "upc": table.get("UPC"),
        "num_reviews": int(table.get("Number of reviews", 0)),
    }


def scrape_details(urls, workers=8):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(parse_detail, urls))
