from nltk.sentiment.vader import SentimentIntensityAnalyzer

new_words = {
    "bearish": -3.0,
    "bullish": 3.0,
}

SIA = SentimentIntensityAnalyzer()
print(SIA.polarity_scores("it is very bullish"))
SIA.lexicon.update(new_words)
print(SIA.polarity_scores("it is very bullish"))
