import scrapy


class ZelfvliegenteamSpider(scrapy.Spider):
    name = 'zelfvliegenteam'
    start_urls = ['https://www.zelfvliegen.nl/team']

    def parse(self, response):
        wrapper = response.xpath('/html/body/div/div/div[3]/div/main/div/div/div/div[2]/div/div/div/section[*]/div[2]/div[2]/div[2]/div/div/p[1]/span/span/span/text()')
        wrapper1 = response.xpath('/html/body/div/div/div[3]/div/main/div/div/div/div[2]/div/div/div/section[*]/div[2]/div[2]/div[2]/div/div/p[2]/span/span/span/text()')
        
        for index, list in enumerate(wrapper):
    
            yield {
                'Naam': list.get().strip(),
                "Functie": wrapper1[index].get().strip(),
                "Organisatie": "Zelfvliegen"
            }
        
        
