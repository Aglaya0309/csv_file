import scrapy
import csv


class LightingnewparsSpider(scrapy.Spider):
    name = "lightingnewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = "divan_lighting_fixed.csv"
        # Открываем файл с BOM (utf-8-sig) и разделителем ";" для Excel
        with open(self.filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Название', 'Цена', 'Ссылка'])

    def parse(self, response):
        lights = response.css("div._Ud0k") or response.css("div[data-testid='product-card']")
        for light in lights:
            item = {
                "name": light.css("div.lsooF span::text").get(),
                "price": light.css("div.pY3d2 span::text").get(),
                "url": light.css("a").attrib["href"]
            }
            # Записываем с разделителем ";" и кодировкой utf-8-sig
            with open(self.filename, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([item['name'], item['price'], item['url']])
            yield item