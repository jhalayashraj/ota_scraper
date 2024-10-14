from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

class HotelSpider:
    def __init__(self, url, proxy = None):
        self.url = url
        self.options = Options()
        options = [
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        for option in options:
            self.options.add_argument(option)

        if proxy:
            self.options.add_argument(f'--proxy-server={proxy}')

    def scrape(self):
        try:
            driver = webdriver.Chrome(options = self.options)
            driver.set_page_load_timeout(30)

            driver.get(self.url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            hotel_listings = soup.find_all('li', class_=lambda class_: class_ and 'relative ml-1 mr-4 flex shrink-0 pt-[5px]' in class_)

            hotels = []
            for hotel in hotel_listings:
                hotel_name_element = hotel.find('span', class_=lambda class_: class_ and 'text-lg font-bold text-gray-800' in class_)
                name = hotel_name_element.text.strip() if hotel_name_element else "N/A"

                location_element = hotel.find('div', class_=lambda class_: class_ and 'block truncate text-sm text-gray-600' in class_)
                location = location_element.text.strip() if location_element else "N/A"

                price_element = hotel.find('span', class_=lambda class_: class_ and 'text-xl font-bold' in class_)
                price = price_element.text.strip() if price_element else "N/A"

                room_type_element = hotel.find('span', class_=lambda class_: class_ and 'inline-block' in class_)
                room_type = room_type_element.text.strip() if room_type_element else "N/A"
                hotels.append({ 'name': name, 'location': location, 'price': price, 'room_type': room_type })

            return hotels

        except TimeoutException:
            print("Timeout occurred while loading the page")
        except WebDriverException as e:
            print(f"WebDriver exception occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if hasattr(self, 'driver'):
                self.driver.quit()

        return []

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
