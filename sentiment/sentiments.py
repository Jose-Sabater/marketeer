# in this module you mostly just catch the sentiment and return it
import pandas as pd
import sys
from scraper import rss_scraper, scrape_google
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sys.path.append("..")
sent_analyzer = SentimentIntensityAnalyzer()
RSS_URL = "https://finance.yahoo.com/news/rssindex"


def ggl_sent_analyzer(keyword: str, content: str) -> list[str]:
    ggl_news_list = scrape_google.main(keyword)
    ggl_sent_list = []
    for article in ggl_news_list:
        _sent = sent_analyzer.polarity_scores(article[content])
        _sent[content] = article[content]
        ggl_sent_list.append(_sent)
    print(ggl_sent_list)


def check_sensitivity(sentence: str) -> dict[float]:
    pos = sent_analyzer.polarity_scores(sentence)["pos"]
    neg = sent_analyzer.polarity_scores(sentence)["neg"]
    neu = sent_analyzer.polarity_scores(sentence)["neu"]
    comp = sent_analyzer.polarity_scores(sentence)["compound"]
    return [pos, neu, neg, comp]


def stock_ggl_sentiment(keyword: str) -> tuple[pd.DataFrame, dict[float]]:
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
    # print(ggl_news_df[["pos", "neu", "neg", "compound"]].describe())
    stats_news = ggl_news_df[["pos", "neu", "neg", "compound"]].describe()
    print(stats_news)
    _sentiment_summary = ggl_news_df[["pos", "neu", "neg", "compound"]].mean()
    sentiment_summary = _sentiment_summary.to_dict()
    print(sentiment_summary)

    # if ggl_news_df["pos"].mean(axis=0) > ggl_news_df["neg"].mean(axis=0):
    #     print("has a positive sentiment")
    # else:
    #     print("has a negative sentiment")

    return ggl_news_df, sentiment_summary


def yahoo_rss_sentiment() -> dict[str]:
    yh_sent_dict = []
    for title in rss_scraper.get_titles(RSS_URL):
        yahoo_sent = sent_analyzer.polarity_scores(title)
        yahoo_sent["title"] = title
        yh_sent_dict.append(yahoo_sent)

    return yh_sent_dict


if __name__ == "__main__":
    yahoo_rss_sentiment()
