import scrapy
import csv
from urllib.parse import urljoin


class LightingnewparsSpider(scrapy.Spider):
    name = "lightingnewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = "divan_lighting_fixed.csv"

        with open(self.filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Название', 'Цена', 'Ссылка'])

    def parse(self, response):
        lights = response.css("div._Ud0k") or response.css("div[data-testid='product-card']")
        for light in lights:
            item = {
                "name": light.css("div.lsooF span::text").get(),
                "price": light.css("div.pY3d2 span::text").get(),
                "url": urljoin("https://www.divan.ru", light.css("a").attrib["href"])
            }

            with open(self.filename, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([item['name'], item['price'], item['url']])

            yield item