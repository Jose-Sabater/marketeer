#  Scrapes RSS data from any RWSS feed
import feedparser

rss_url = "https://finance.yahoo.com/news/rssindex"


def get_titles(url: str) -> list[str]:
    print(f"Getting {rss_url} titles...")
    entries = feedparser.parse(url)["entries"]
    titles = []
    for i, entry in enumerate(entries):
        # print(i, entry["title"])
        titles.append(entry["title"])
    return titles
