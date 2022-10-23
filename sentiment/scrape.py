from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

root = "https://google.com"
link = "https://www.google.com/search?q=trump&sxsrf=ALiCzsbQk2to4N259vd7Gg-iHM_tF-ySCA:1666453257763&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjfsNqTlvT6AhVji8MKHdaHDQMQ_AUoAXoECAEQAw&biw=1920&bih=941&dpr=1"
headers = {"User-Agent": "Mozilla/5.0"}


def news(link):
    req = Request(link, headers=headers)
    webpage = urlopen(req).read()
    # print(webpage)

    # With this we get a list of all webs that have articles on what we are looking for
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, "html.parser")
        print(soup)
        # for item in soup.find_all("div", attrs={"class": "kCrYT"}):
        for item in soup.find_all(
            "div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"}
        ):
            raw_link = item.find("a", href=True)["href"]
            link = raw_link.split("/url?q=")[1].split("&sa=U&")[0]
            title = item.find(
                "div", attrs={"class": "BNeawe vvjwJb AP7Wnd"}
            ).get_text()
            title = title.replace(",", "")  # remove commas
            description = item.find(
                "div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}
            ).get_text()
            time = description.split("...")[1]
            description = description.split("...")[0]
            description.replace(",", "")
            print(f"Title : {title}")
            print(f"Description : {description}")
            print(f"Time : {time}")
            print(f"Link to text : {link}")
            # print(item)

            with open("data.csv", "a") as document:
                document.write(f"{title}, {time}, {description}, {link}\n")

        next = soup.find("a", attrs={"aria-label": "Nästa sida"})
        next = next["href"]

        link = root + next
