import scrapy

class VliegveldenLijstSpider(scrapy.Spider):
    name = 'vliegvelden_lijst'
    start_urls = ['https://nl.wikipedia.org/wiki/Lijst_van_vliegvelden_in_Nederland']

    def parse(self, response):
        table = response.xpath('//*[@class="wikitable"]//tbody')
        rows = table.xpath('//tr')
        # links = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[*]/td[5]/small/span/a/@href').getall()
        def containsNumber(value):
            for character in value:
                if character.isdigit():
                    return True
            return False

        for row in rows:
            locatie = row.xpath('td[1]//text()').extract_first()
            naam = row.xpath('td[4]//text()').extract_first()
            link = row.xpath('td[5]/small/span/a/@href | td[5]/a/@href').extract_first()
            # print(row.xpath('td[5]').attrib['href'])
            if not containsNumber((str(locatie))):
                if not "Bronnen" in str(locatie):
                    if locatie is not None:





                        
                        yield {
                            # "url": link,
                            "locatie": locatie,
                            "naam": naam
                        }
                        yield response.follow(link, callback=self.getCoords)

    def getCoords(self, response):
        print(f"RESPONSE: {response}")

        wrapper = response.xpath('//*[@class="geo"]')

        for item in wrapper:
            lat = item.xpath('span[1]/text()').get() 
            long = item.xpath('span[2]/text()').get()
            

        with open('output.csv', 'a') as file:  # Use file to refer to the file object
            file.write(f'{lat}, {long}\n')


        
        
