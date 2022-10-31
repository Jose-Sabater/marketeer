from sentiment import sentiments


def main():
    # sentiments.yahoo_rss_sentiment()
    # sentiments.ggl_sent_analyzer("amazon", "description")
    sentiments.stock_ggl_sentiment("amazon")


if __name__ == "__main__":
    main()
