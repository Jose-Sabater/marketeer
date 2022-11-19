# in this module you mostly just catch the sentiment and return it
import pandas as pd
import sys
from scraper import rss_scraper, scrape_google
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sent_analyzer = SentimentIntensityAnalyzer()
sys.path.append("..")

# RSS_URL = "https://finance.yahoo.com/news/rssindex"


def ggl_sent_analyzer(keyword: str, content: str) -> list[str]:
    ggl_news_list = scrape_google.main(keyword)
    ggl_sent_list = []
    for article in ggl_news_list:
        _sent = sent_analyzer.polarity_scores(article[content])
        _sent[content] = article[content]
        ggl_sent_list.append(_sent)
    print(ggl_sent_list)


def check_sensitivity(sentence: str) -> dict[float]:
    """Calculates the polarity scores using VaderSentiment

    Parameters:
        sentence (str): the string you want to check the sentiment

    Returns:
        (dict[float]) : a dictionary witht he sentiment values pos, neg, neu,
        compound as per https://github.com/cjhutto/vaderSentiment
    """
    pos = sent_analyzer.polarity_scores(sentence)["pos"]
    neg = sent_analyzer.polarity_scores(sentence)["neg"]
    neu = sent_analyzer.polarity_scores(sentence)["neu"]
    comp = sent_analyzer.polarity_scores(sentence)["compound"]
    return [pos, neu, neg, comp]


def stock_ggl_sentiment(keyword: str) -> tuple[pd.DataFrame, dict[float]]:
    """Check the sentiment of a google news search

    Parameters:
        keyword (str): the information you want to look up in google news

    Returns:
        ggl_news_df (pd.Dataframe): a dataframe with your google news
        sentiment_summary (dict[float]) : a dictionary with the vader
        sentiment of your search
    """
    ggl_news_df = pd.DataFrame(scrape_google.main(keyword))

    ggl_news_df["pos"] = (
        ggl_news_df["description"].apply(lambda x: check_sensitivity(x)[0])
        + ggl_news_df["title"].apply(lambda x: check_sensitivity(x)[0])
    ) / 2
    ggl_news_df["neu"] = (
        ggl_news_df["description"].apply(lambda x: check_sensitivity(x)[1])
        + ggl_news_df["title"].apply(lambda x: check_sensitivity(x)[1])
    ) / 2
    ggl_news_df["neg"] = (
        ggl_news_df["description"].apply(lambda x: check_sensitivity(x)[2])
        + ggl_news_df["title"].apply(lambda x: check_sensitivity(x)[2])
    ) / 2
    ggl_news_df["compound"] = (
        ggl_news_df["description"].apply(lambda x: check_sensitivity(x)[3])
        + ggl_news_df["title"].apply(lambda x: check_sensitivity(x)[3])
    ) / 2

    print(ggl_news_df.head())
    stats_news = ggl_news_df[["pos", "neu", "neg", "compound"]].describe()
    print(stats_news)
    _sentiment_summary = ggl_news_df[["pos", "neu", "neg", "compound"]].mean()
    sentiment_summary = _sentiment_summary.to_dict()
    print(sentiment_summary)

    return ggl_news_df, sentiment_summary


def yahoo_rss_sentiment(rss_url) -> dict[str]:
    """Returns the titles and vader sentiment of the selected rss

    Parameters:
        rss_url (str): a valid RSS URL

    Returns:
        Titles from the RSS feed and their sentiment (List[Dict[str]])
    """
    yh_sent_dict = []
    for title in rss_scraper.get_titles(rss_url):
        yahoo_sent = sent_analyzer.polarity_scores(title)
        yahoo_sent["title"] = title
        yh_sent_dict.append(yahoo_sent)

    return yh_sent_dict


if __name__ == "__main__":
    yahoo_rss_sentiment()
