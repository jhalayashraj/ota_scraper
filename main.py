from scraper.spider import HotelSpider
from scraper.proxy_rotator import ProxyRotator
import csv

def main():
    url = "https://www.ikyu.com/?are=120240&lgp=1039&ppc=2&rc=1"
    proxies = [
        "43.134.33.254:3128",
        "103.67.237.214:3128",
        "160.86.242.23:8080"
    ]

    proxy_rotator = ProxyRotator(proxies)
    all_hotels = []

    for _ in range(len(proxies)):  # try each proxy
        proxy = proxy_rotator.get_proxy()
        # as these are free proxies and if it stops working
        # we can replace it with the new one or just remove
        # the proxy parameter from below to run script without proxy.
        spider = HotelSpider(url, proxy)
        hotels = spider.scrape()

        if hotels:
            all_hotels.extend(hotels)
            break # if successful, stop trying other proxies
        else:
            print(f"Scraping failed with proxy {proxy}. Trying next proxy.")

    if all_hotels:
        # generate CSV report with extracted data
        with open('report.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'location', 'room_type', 'price'])
            writer.writeheader()
            for hotel in all_hotels:
                writer.writerow({
                    'name': hotel['name'],
                    'location': hotel['location'],
                    'room_type': hotel['room_type'],
                    'price': hotel['price']
                })
        print(f"Successfully scraped {len(all_hotels)} hotels. Data saved to report.csv")
    else:
        print("Scraping failed with all proxies. No data to save.")

if __name__ == "__main__":
    main()
