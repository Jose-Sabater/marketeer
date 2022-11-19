# Scrape google news from a specific keyword
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

root = "https://google.com"
keyword = "biden"
# link = f"https://www.google.com/search?q={keyword}&sxsrf=ALiCzsbQk2to4N259vd7Gg-iHM_tF-ySCA:1666453257763&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjfsNqTlvT6AhVji8MKHdaHDQMQ_AUoAXoECAEQAw&biw=1920&bih=941&dpr=1"
headers = {"User-Agent": "Mozilla/5.0"}


def main(keyword, loops: int = 6) -> list[dict[str]]:
    print("Started Scraping................................")
    news_list = []
    link = f"https://www.google.com/search?q={keyword}&sxsrf=ALiCzsbQk2to4N259vd7Gg-iHM_tF-ySCA:1666453257763&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjfsNqTlvT6AhVji8MKHdaHDQMQ_AUoAXoECAEQAw&biw=1920&bih=941&dpr=1"
    for i in range(loops - 1):
        _news_list, next_link = news(link)
        link = next_link
        news_list.extend(_news_list)
    return news_list


def news(link: str, save_csv: int = 0) -> list[dict[str]]:
    req = Request(link, headers=headers)
    webpage = urlopen(req).read()
    # With this we get a list of all webs that have articles on what we are
    # looking for
    with requests.Session() as c:

        news_list = []
        soup = BeautifulSoup(webpage, "html.parser", from_encoding="utf-8")
        # print(soup.original_encoding)
        # print(soup)
        # for item in soup.find_all("div", attrs={"class": "kCrYT"}):
        for item in soup.find_all(
            "div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"}
        ):
            news_dict = {}
            try:

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
                description = description.replace(",", "")
                # print(f"Title : {title}")
                # print(f"Description : {description}")
                # print(f"Time : {time}")
                # print(f"Link to text : {link}")

                # Store info in dictionary
                news_dict["title"] = title
                news_dict["description"] = description
                news_dict["time"] = time
                news_dict["link"] = link
                news_list.append(news_dict)
                # pass into the list
                # news_list.append(news_dict)

                # write to file, only do if certain opption
                if save_csv == 1:
                    with open("data.csv", "a") as document:
                        # if "För" not in time:
                        if "För" not in time:
                            pass
                        else:
                            document.write(
                                f"{title}, {time}, {description}, {link}\n"
                            )
            # Error catching and skipping
            except UnicodeEncodeError:
                print("There was a unicoder error")
                pass

            except IndexError:
                print("Something went wrong, IndexError")
                pass

            except TypeError:
                print("End of the content")

        # Scrape all available pages
        next = soup.find("a", attrs={"aria-label": "Nästa sida"})
        next = next["href"]
        next_link = root + next
        # news(link)

    return news_list, next_link


if __name__ == "__main__":
    print(main(keyword))
