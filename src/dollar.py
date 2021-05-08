import requests
import bs4
import time


class Currency:
    def __init__(self):
        self.last_sec = 0
        self.currency_link = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'}
        self.currency = 0
        self.update()

    def update_currency_price(self):
        full_page = requests.get(self.currency_link, headers=self.headers)

        soup = bs4.BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        self.currency = float(convert[0].text.replace(",", "."))

    def update(self):
        if time.time() - self.last_sec > 5:
            self.update_currency_price()
            self.last_sec = time.time()

    def get_exchange_rate(self):
        self.update()
        return int(self.currency)
