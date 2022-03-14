import scrapy


class OlieonlineSpider(scrapy.Spider):
    name = 'olieonline'
    start_urls = ['https://www.olieonline.nl/shell-olie/aeroshell/']

    def parse(self, response):

        wrapper = response.css('#products-list')

        name = wrapper.xpath('li/div[2]/div/h2/a/text()').getall()

        desc = wrapper.xpath('li/div[2]/div/div/h4/text()').getall()
        price_excl = wrapper.xpath('li/div[3]/div/p/span[2]/span[2]/text()').getall()
        price_incl = wrapper.xpath('li/div[3]/div/p/span[3]/span[2]/text()').getall()
        
        for index, item in enumerate(name):
            calc = float(price_incl[index].replace('\n€\xa0', '').replace(',', '.').strip()) - float(price_excl[index].replace('\n€\xa0', '').replace(',', '.').strip())
            yield {
                "name": item,
                "description": desc[index],
                "price_excl": float(price_excl[index].replace('\n€\xa0', '').replace(',', '.').strip()),
                "price_incl": float(price_incl[index].replace('\n€\xa0', '').replace(',', '.').strip()),
                "type": str(item).replace('Shell Aeroshell', '').strip().split(' ')[0].strip(),
                "btw": calc
            }

        next_page = response.css('a.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
