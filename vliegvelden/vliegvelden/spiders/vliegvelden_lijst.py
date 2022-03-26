import scrapy
from .gps_to_lonlat import parse_dms_string

class VliegveldenLijstSpider(scrapy.Spider):
    name = 'vliegvelden_lijst'
    start_urls = ['https://nl.wikipedia.org/wiki/Lijst_van_vliegvelden_in_Nederland']


    def parse(self, response):
        # Hier pak je de body van de table
        table = response.xpath('//*[@class="wikitable"]//tbody')

        # Vervolgens pak je hier alle rijen die in die table zitten
        rows = table.xpath('//tr')

        # Dit is een functie die coontroleert of een waarde een getal
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

        #    als die niet een getal is, ga dan verder 
            if not containsNumber((str(locatie))):
                # Als bronnen er niet is, ga dan verder 
                if not "Bronnen" in str(locatie):
                    # Als locatie niet null is 
                    if locatie is not None:
                        # Hier worden de wiki coords,omgezet naar speciale cords voor kibana 
                        coordsAll = parse_dms_string(coords)

                        yield {
                            "locatie": locatie,
                            "naam": naam,
                            "Latitude": coordsAll[0],
                            "Longitude": coordsAll[1]
                        }
