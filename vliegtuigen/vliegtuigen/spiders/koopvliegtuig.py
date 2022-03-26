
import scrapy


class KoopvliegtuigSpider(scrapy.Spider):
    name = 'koopvliegtuig'
    start_urls = ['https://www.aircraft24.nl/search/index.htm?dosearch=1']
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}

    def parse(self, response):

        wrapper = response.xpath('//*[@id="content-table-col-mid"]')
        links = wrapper.xpath('//*[@id="content-table-col-mid"]/a[*]/@href')

        for link in links:
            yield response.follow(link.get(), callback=self.getPlaneInfo)

        next_page = response.css('a.next').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)            
            
    def getPlaneInfo(self, response):
    
        wrapper = response.xpath('//*[@id="content-table-col-mid"]')
        
        for i in wrapper:
            br = i.xpath('/html/body/div[3]/div/table/tr/td[2]/div[2]/table/tr/td[1]/table[2]/tr[2]/td/p').get().replace("\r\n", '').replace('\t', '').replace('<p>', '').replace('</p>', '').split('<br>')
            details = i.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[*]')
            d = []
            for i in details:
                d.append(f"{i.xpath('td[1]/text()').get()} | {i.xpath('td[2]/text()').get()}")
            print(d)
            typeProps = [x for x in d if all(y in x for y in ['Type: | '])][0].replace('Type: | ', '').strip()
            Bouwjaar = [x for x in d if all(y in x for y in ['Bouwjaar:'])][0].replace('Bouwjaar: |', '').strip()
            Location = [x for x in d if all(y in x for y in ['Location:'])][0].replace('Location: |', '').strip().split(',')[0]
            
            filter_data = [x for x in br if all(y in x for y in ['Tel:'])]
            filterDataNone = [x for x in br if all(y not in x for y in ['Tel:'])]
            listToStr = ' '.join([str(elem) for elem in filterDataNone])

            try:
                yield {
                'Naam': str(i.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[1]/h1/text()').get().strip().replace('é', 'e').replace('     ', ''))[0:16],
                'Prijs': int(i.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[2]/text()').get().strip().replace('€ ','').replace('.', '')),
                "Contact_Nummer": str(f"TEL: +{str(filter_data[0]).replace('Tel:', '').replace(' ', '').replace('-', '').replace('+', '').strip()}")[0:20],
                "Contact_Name": str(str(listToStr).replace('<b>', '').replace('</b>', ''))[0:20],
                "Props": typeProps,
                "Bouwjaar": int(Bouwjaar),
                "Location": Location,
                "Dutch": True if Location == "Nederland" else False
            }    
            except:
                pass