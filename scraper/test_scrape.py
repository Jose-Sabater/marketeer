# Another google news scraper from SerpaAPI
from serpapi import GoogleSearch
import json

params = {
    "api_key": "e6d359350b7453de786d5fca4c5fb8c0e7fd1ae8c12ede64f4af194b76494956",  # your serpapi api key
    "engine": "google",  # serpapi parsing engine
    "q": "trump",  # search query
    "gl": "us",  # country from where search comes from
    "tbm": "nws"  # news results
    # other parameters such as language `hl` and number of news results `num`, etc.
}

search = GoogleSearch(params)  # where data extraction happens on the backend
results = search.get_dict()  # JSON - > Python dictionary

for result in results["news_results"]:
    print(json.dumps(results, indent=2))
with open("result.json", "w") as outfile:
    results_out = json.dumps(results, indent=2)
    outfile.write(results_out)
