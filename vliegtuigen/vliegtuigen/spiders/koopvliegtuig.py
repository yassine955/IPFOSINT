
import scrapy
import goslate 


class KoopvliegtuigSpider(scrapy.Spider):
    name = 'koopvliegtuig'
    start_urls = ['https://www.aircraft24.nl/search/index.htm?dosearch=1']
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 3}

    def parse(self, response):
        # gs = goslate.Goslate()
        wrapper = response.xpath('//*[@id="content-table-col-mid"]/a[*]')
    
        for index, item in enumerate(wrapper):
            title = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[1]/text()').get()).strip()
            price = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[1]/span/text()').get()).strip().replace('€ ', '').replace('.', '')
            description = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[2]/text()').get()).strip().split(";")
            location = []


            # HIER MOET CODE KOMEN VAN NUMMER


            try:
                for x in description:
                    if "Location" in x:
                        location.append(x.split(',')[0].replace('Location: ', '').strip())

                for p in location:
                    
                    yield {
                        'name': title,
                        'price': int(price),
                        'location': p
                    }
            except:
                pass 
        next_page = response.css('a.next').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)    
          





    # def getPlaneInfo(self, response):
       
    #     wrapper = response.xpath('//*[@id="content-table-col-mid"]')
        
    #     for item in wrapper:
    #         name = item.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[1]/h1/text()').get()
    #         price = item.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[2]/text()').get().replace('€ ','')
    #         data = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[*]')
    #         number = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[2]/tr[2]/td/p/text()[2]').get().strip()
    #         contactName = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[2]/tr[2]/td/p/text()[1]').get().strip() 
          
    #         d = []
                 
    #         for index, item in enumerate(data):               
    #             dataTitle = item.xpath(f'//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[{index}]/td[1]/text()').get()
    #             dataInput = item.xpath(f'//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[{index}]/td[2]/text()').get()
                
    #             if str(dataTitle).strip().replace(':', '') == "Bouwjaar":
    #                 d.append({
    #                     f"{str(dataTitle).strip().replace(':', '')}": int(f"{str(dataInput).strip()}")
    #                 })
    #             else:
    #                 d.append({
    #                     f"{str(dataTitle).strip().replace(':', '')}": f'{str(dataInput).strip()}',
    #                 })
                   

    #         yield {
    #             'name': name,
    #             'price': int(str(price).replace('.', '')),
    #             'contact_number': number,
    #             'contactName': contactName,
    #             'details': list(d),
    #         }
