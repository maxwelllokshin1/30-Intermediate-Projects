from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def search(name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": name,
        "quotes_count": 1,
        "news_count": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    result = response.json()

    if result["quotes"]:
        ticker = result["quotes"][0]["symbol"]
        name = result["quotes"][0]["shortname"]
        # print(f"Company: {name}\nTicker: {ticker}")
        return ticker
    else:
        return None


def webScraper(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    # Get the HTML content
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    ticker = soup.find("h1", class_="yf-xxbei9")
    print(f"\n{ticker.text}\n{'=' * 40}")
    all_info = soup.find("div", class_="container yf-1jj98ts").find_all('li')
    for info in all_info:
        cols = info.find_all('span')
        if len(cols) == 2:
            print(f"{cols[0].get_text().strip().ljust(25)}: {cols[1].get_text().strip()}")
    

def main():
    company = input("Full Company Name: ")
    ticker = search(company)
    if ticker == None:
        print("DNE")
        return
    url = f"https://finance.yahoo.com/quote/{ticker}/"
    webScraper(url)

if __name__ == "__main__":
    main()