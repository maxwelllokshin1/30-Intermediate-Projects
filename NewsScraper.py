from urllib.request import urlopen
from bs4 import BeautifulSoup

def webScraper(url):
    articles = []
    # Get the HTML content
    response = urlopen(url)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'lxml')

    titles = soup.find_all("a", class_="container__link container__link--type-article container_lead-plus-headlines__link")
    for title in titles:
        headline_div = title.find("span", class_="container__headline-text")
        if headline_div:
            articles.append({"Headline": headline_div.get_text(strip=True), "Link": "https://www.cnn.com" + title['href']})

    return articles

def main():
    url = "https://edition.cnn.com/world"
    articles = webScraper(url)
    for idx, article in enumerate(articles[:10], 1):  # Limit to top 10 for brevity
        print(f"{idx}. {article['Headline']}")
        print(f"Link: {article['Link']}")
        print()
    
if __name__ == "__main__":
    main()