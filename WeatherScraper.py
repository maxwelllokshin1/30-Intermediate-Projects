from urllib.request import urlopen
from bs4 import BeautifulSoup

def webScraper(url):
    # Get the HTML content
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    # Find the temperature and condition
    temperature = soup.find("div", class_="h2").text.strip() # find first instance of a div with class h2
    weather_info = soup.find("div", class_="bk-focus__qlook")  # find first instance of div with class bk-focus__qlook
    details = weather_info.find_all("p") # find all the details inside weather_info
    print(f"Temperature: {temperature}")

    # parse the text so it is readable
    for info in details:
        raw_html = info.decode_contents() # remove all <br>
        html_parts = raw_html.split("<br/>") # remove all <br/>

        for part in html_parts:
            text = BeautifulSoup(part, 'lxml').get_text().strip() # remove unessecary spaces or <>
            if text:
                print(text) # if the text exists print it

def main():
    url = "https://www.timeanddate.com/weather/uk/london"
    print("Conditions for London, UK")
    webScraper(url)
    
if __name__ == "__main__":
    main()