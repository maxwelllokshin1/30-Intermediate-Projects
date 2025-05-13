from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def search(name):
    url = "https://www.timeanddate.com/weather/search/"
    params = {
        "query": name,
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    sections = soup.find_all("section", class_="fixed")
    arr_list = [
        row
        for section in sections
        for table in section.find_all("table")
        for row in table.find_all("tr")
    ]
    for row in arr_list:
        if row.find("th"):
            continue

        first_td = row.find("td")
        if first_td:
            link = first_td.find("a")
            if link and link.get("href"):
                return link["href"]


def webScraper(url):
    weather_values = []
    # Get the HTML content
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    # Find the temperature and condition
    title = soup.find("h1", class_="headline-banner__title")
    
    temperature = soup.find("div", class_="h2").text.strip() # find first instance of a div with class h2
    weather_values.append({"Key": "Temperature", "Value": temperature})

    weather_info = soup.find("div", class_="bk-focus__qlook")  # find first instance of div with class bk-focus__qlook
    details = weather_info.find_all("p") # find all the details inside weather_info

    # parse the text so it is readable
    for info in details:
        raw_html = info.decode_contents() # remove all <br>
        html_parts = raw_html.split("<br/>") # remove all <br/>

        for part in html_parts:
            text = BeautifulSoup(part, 'lxml').get_text().strip() # remove unessecary spaces or <>
            if ":" in text:
                key, value = map(str.strip, text.split(":", 1))
                weather_values.append({"Key": key, "Value": value})

    print(f"\n{title.text}\n{'=' * 40}")
    return weather_values

def main():
    location = input("Location: ")
    link = search(location)

    url = "https://www.timeanddate.com" + link
    weather_values = webScraper(url)
    for val in weather_values:
        print(f"{val['Key'].ljust(25)}: {val['Value'].ljust(25)}")
    
if __name__ == "__main__":
    main()
