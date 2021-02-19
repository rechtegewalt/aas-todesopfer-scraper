import re

import dataset
import get_retries
from bs4 import BeautifulSoup
from dateparser import parse

db = dataset.connect("sqlite:///data.sqlite")

tab_incidents = db["incidents"]
tab_sources = db["sources"]
tab_chronicles = db["chronicles"]


tab_chronicles.upsert(
    {
        "iso3166_1": "DE",
        "region": "Deutschland",
        "chronicler_name": "Todesopfer rechter Gewalt, Amadeu Antonio Stiftung",
        "chronicler_description": """Seit Jahren beklagt die Amadeu Antonio Stiftung die große Diskrepanz zwischen der Anerkennung von Todesopfern rechter Gewalt durch staatliche Behörden und der Zählung durch unabhängige Organisationen sowie Journalistinnen und Journalisten.

Wo von der Bundesregierung lediglich 106 Tötungsdelikte als rechts motiviert gewertet werden, ergeben Recherchen der Amadeu Antonio Stiftung eine weitaus höhere Zahl: Mindestens 213 Todesopfer rechter Gewalt seit dem Wendejahr 1990 sowie 13 weitere Verdachtsfälle.

Die Recherche zu den Todesopfern rechter Gewalt stützt sich in der Regel auf Medienberichte, Monitoring durch Opferberatungsstellen und Recherchearbeiten von Journalistinnen und Journalisten sowie Gedenkinitiativen.""",
        "chronicler_url": "https://www.amadeu-antonio-stiftung.de",
        "chronicle_source": "https://www.amadeu-antonio-stiftung.de/todesopfer-rechter-gewalt/",
        "rgf_version": 1,
    },
    ["chronicler_name"],
)


BASE_URL = "https://www.amadeu-antonio-stiftung.de/todesopfer-rechter-gewalt/"


def fix_date_typo(x):
    """
    fix date typos such as 14,12.2020 or 01.12,2020
    """
    x = re.sub(r"(\d\d),(\d\d.\d\d\d\d)", r"\1.\2", x)
    x = re.sub(r"(\d\d.\d\d),(\d\d\d\d)", r"\1.\2", x)
    return x


def fetch(url):
    html_content = get_retries.get(url, verbose=True, max_backoff=128).text
    soup = BeautifulSoup(html_content, "lxml")
    return soup


def process_report(url, data):
    entry = fetch(url)

    title = entry.select_one("h1.entry-title").get_text().strip()
    description = "\n\n".join(
        [x.get_text().strip() for x in entry.select(".entry-content p")]
    )
    rg_id = "aas-trg-" + entry.select_one("article").get("id")
    sources = []
    source_link = entry.select_one(".socials .text-grey-light a")
    if source_link:
        sources.append(
            {"rg_id": rg_id, "name": source_link.get_text().strip(), "url": source_link.get("href")}
        )

    data["chronicler_name"] = "Todesopfer rechter Gewalt, Amadeu Antonio Stiftung"
    data["description"] = description
    data["title"] = title
    data["rg_id"] = rg_id

    # print(data)

    tab_incidents.upsert(data, ["rg_id"])

    for x in sources:
        tab_sources.upsert(x, ["rg_id", "name", "date"])


initial_soup = fetch(BASE_URL)

for x in initial_soup.select("article"):
    left_col = x.select_one("div")
    date = left_col.select_one(".bigdate").get_text().strip()
    url = x.select_one("a.text-primary").get("href")
    rows = [x.get_text().strip() for x in left_col.select(".text-grey-light")]
    date = parse(date, languages=["de"])

    city = rows[0]
    official = False
    age = 1

    if len(rows) > 1:
        age = rows[1]

    if len(rows) == 3:
        official = "(staatlich anerkannt)" in rows[2]

    process_report(url, dict(url=url, age=age, official=official, date=date, city=city))


# last_page = re.findall(
#     r"\d+", initial_soup.select_one("li.pager-last.last a").get("href")
# )[0]

# last_page = int(last_page)

# process_page(initial_soup)

# print(last_page)

# i = 1
# while i <= last_page:
#     url = BASE_URL + f"?page={i}"
#     print(url)
#     process_page(fetch(url))
#     i += 1
