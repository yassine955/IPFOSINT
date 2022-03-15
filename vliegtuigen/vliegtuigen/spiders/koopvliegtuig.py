
import scrapy
import goslate 


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

        naam = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[2]/table[1]/tbody/tr/td[1]/h1/text()').get()

        
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
    
  
  
  
            # yield {
            #     'Naam': i.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[1]/h1/text()').get().strip().replace('é', 'e'),
            #     'Prijs': int(i.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[2]/text()').get().strip().replace('€ ','').replace('.', '')),
            #     'Contact': i.xpath('/html/body/div[3]/div/table/tr/td[2]/div[2]/table/tr/td[1]/table[2]/tr[2]/td/p').get().replace("\r\n", '').replace('\t', '').replace('<p>', '').replace('</p>', ''),
            #     "Contact_Nummer": str(filter_data[0]).replace('Tel:', '')
            # }

        # for item in wrapper:
        #     name = item.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[1]/h1/text()').get()
        #     price = item.xpath('/html/body/div[3]/div/table/tr/td[2]/table[1]/tr/td[2]/text()').get().replace('€ ','')
        #     data = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[*]')
        #     number = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[2]/tr[2]/td/p/text()[2]').get().strip()
        #     contactName = item.xpath('//*[@id="addetailoverview"]/tr/td[1]/table[2]/tr[2]/td/p/text()[1]').get().strip() 
            
        #     # d = []
                    
        #     # for index, item in enumerate(data):               
        #     #     dataTitle = item.xpath(f'//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[{index}]/td[1]/text()').get()
        #     #     dataInput = item.xpath(f'//*[@id="addetailoverview"]/tr/td[1]/table[1]/tr[{index}]/td[2]/text()').get()
                
        #     #     if str(dataTitle).strip().replace(':', '') == "Bouwjaar":
        #     #         d.append({
        #     #             f"{str(dataTitle).strip().replace(':', '')}": int(f"{str(dataInput).strip()}")
        #     #         })
        #     #     else:
        #     #         d.append({
        #     #             f"{str(dataTitle).strip().replace(':', '')}": f'{str(dataInput).strip()}',
        #     #         })
                    

        #     yield {
        #         'Naam': name,
        #         'Prijs': int(str(price).replace('.', '')),
        #         'Contact_Nummer': number,
        #         'Contact_Naam': contactName,
        #     }


        # # gs = goslate.Goslate()
        # wrapper = response.xpath('//*[@id="content-table-col-mid"]/a[*]')
    
        # for index, item in enumerate(wrapper):
        #     title = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[1]/text()').get()).strip()
        #     price = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[1]/span/text()').get()).strip().replace('€ ', '').replace('.', '')
        #     description = str(item.xpath(f'//*[@id="content-table-col-mid"]/a[{index}]/div[2]/div[2]/text()').get()).strip().split(";")
        #     location = []


        #     # HIER MOET CODE KOMEN VAN NUMMER

 
        
          





    
