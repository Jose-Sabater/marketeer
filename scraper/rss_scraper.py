import feedparser

rss_url = "https://finance.yahoo.com/news/rssindex"


def get_titles(url: str) -> list[str]:
    entries = feedparser.parse(url)["entries"]
    print("parser_result")
    titles = []
    for i, entry in enumerate(entries):
        # print(i, entry["title"])
        titles.append(entry["title"])
    return titles
