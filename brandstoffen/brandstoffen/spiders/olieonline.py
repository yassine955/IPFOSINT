import scrapy


class OlieonlineSpider(scrapy.Spider):
    name = 'olieonline'
    start_urls = ['https://www.olieonline.nl/shell-olie/aeroshell/']

    def parse(self, response):
        # Pak de gehele contianer van alle producten 
        wrapper = response.css('#products-list')

        # Haal alle namen op van die container 
        name = wrapper.xpath('li/div[2]/div/h2/a/text()').getall()

        # Haal alle beschrijvingen op 
        desc = wrapper.xpath('li/div[2]/div/div/h4/text()').getall()

        # Haal alle prijzen op 
        price_excl = wrapper.xpath('li/div[3]/div/p/span[2]/span[2]/text()').getall()
        price_incl = wrapper.xpath('li/div[3]/div/p/span[3]/span[2]/text()').getall()
        
        # Een for loop over alle namen die in de container beschikbaar zijn 
        # Index is de waarde van de volgorde 0 , 1 , 2  
        for index, item in enumerate(name):
            # Pak de inc prijs, van de het product 
            # Dit berekent de BTW 
            calc = float(price_incl[index].replace('\n€\xa0', '').replace(',', '.').strip()) - float(price_excl[index].replace('\n€\xa0', '').replace(',', '.').strip())
            
            yield {
                "name": item,
                "description": desc[index],
                "price_excl": float(price_excl[index].replace('\n€\xa0', '').replace(',', '.').strip()),
                "price_incl": float(price_incl[index].replace('\n€\xa0', '').replace(',', '.').strip()),
                # Pak alle types, door shell aeroshell te vervangen en te splitten op spatie, en vervolgens de eerste waarde te pakken 
                "type": str(item).replace('Shell Aeroshell', '').strip().split(' ')[0].strip(),
                "btw": calc
            }
        # Pak de next page button om naar de volgende pagina te gaan 
        next_page = response.css('a.next').attrib['href']
        # Als er een next page is gevonden, voer dan de response.follow functie uit en ga naar de volgende pagina 
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
