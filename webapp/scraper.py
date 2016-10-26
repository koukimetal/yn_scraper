import urllib.request
from bs4 import BeautifulSoup


def extract_news():
    req = urllib.request.Request('http://news.yahoo.co.jp/')
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        soup = BeautifulSoup(the_page, "html.parser")
        news = soup.find_all(class_="topics")[0].find_all(class_="ttl")
        res = []
        for info in news:
            res.append({
                'title': info.a.text,
                'url': info.a.get('href')
            })

        return res


if __name__ == '__main__':
    result = extract_news()
    print(result)