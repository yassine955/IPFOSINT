import scrapy
from .gps_to_lonlat import parse_dms_string

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
            coords = row.xpath('td[5]/small/span/a/text() | td[5]/a/text()').extract_first()
            coords = str(coords).replace("' ", "'").replace(' NB', 'N').replace(' OL', 'E').replace('° ', '°').replace('″', '"').replace("'N", '"N').replace("'E", '"E').replace('′ ', "'").replace(' WL', "W").replace(' N', 'N').replace('"NB', '"N').replace("'OL", '"E').replace('N ', "N, ").replace('" E', '"E').replace(' °', '°').strip()

            if not containsNumber((str(locatie))):
                if not "Bronnen" in str(locatie):
                    if locatie is not None:
                        # print(VliegveldenLijstSpider.conversion(lat), VliegveldenLijstSpider.conversion(lon) )
                        # INPUT = """52°49'07"N, 4°55'43"E"""
                        # INPUT = f"""{coords}"""
                        # yield {
                        #     "INPUT": INPUT
                        # }
                        # print(coords)
                        
                       
                        # coordi.append(coords)

                        # print(coordi)
                        #(f"""{x}""")) 

                        coordsAll = parse_dms_string(coords)

                        yield {
                            "locatie": locatie,
                            "naam": naam,
                            "Latitude": coordsAll[0],
                            "Longitude": coordsAll[1]
                        }
                       
                        # yield response.follow(link, callback=self.getCoords)


    # def getCoords(self, response):
        
    #     wrapper = response.xpath('//*[@class="geo"]')

    #     for item in wrapper:
    #         lat = item.xpath('span[1]/text()').get() 
    #         long = item.xpath('span[2]/text()').get()
        
    #     with open('output.csv', 'a') as file:  # Use file to refer to the file object
    #         file.write(f'{lat}, {long}\n')


        
        
