from sentiment import sentiments


def main():
    # print(
    #     sentiments.yahoo_rss_sentiment(
    #         "https://finance.yahoo.com/news/rssindex"
    #     )
    # )
    # sentiments.ggl_sent_analyzer("amazon", "description")
    sentiments.stock_ggl_sentiment("amazon")


if __name__ == "__main__":
    main()
