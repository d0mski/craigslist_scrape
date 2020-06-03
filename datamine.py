# import packages
import scrapy

# Define Queries

query = input("What do you want your search criteria to be? ").lower()
query = query.replace(' ','+')

# Create dictionary for sections of Craigslist

sections = {'ata':'antiques', 'ppa':'appliances', 'ara':'artsandcrafts', 'sna':'atvsutvssnowmobiles',
            'pta':'autoparts', 'ava':'aviation', 'baa':'babyandkidstuff','bar':'barter', 'haa':'healthandbeauty',
            'bip':'bicycleparts', 'bia':'bicycles','bpa':'itemparts','bka':'booksandmagazines','bfa':'business',
            'cta':'carsandtrucks','ema':'cds', 'moa':'cellphones', 'cla':'clothingandaccessories',
            'cba':'collectibles', 'syp':'computerparts','sya':'computers','ela':'electronics','gra':'farmandgarden',
            'zip':'free','fua':'furniture','gms':'garagesales','foa':'general','hva':'heavyequipment',
            'hsa':'household', 'jwa':'jewelry', 'maa':'materials', 'mpa':'motorcycleparts',
            'mca':'motorcycles','msa':'musicalinstruments','pha':'photoandvideo','rva':'recreationalvehicles',
            'sga':'sportinggoods','tia':'tickets','tla':'tools','taa':'toysandgames','tra':'trailers',
            'vga':'videogaming','waa':'wanted','wta':'wheelsandtires'}

values = []

for key, value in sections.items():
    values.append(value)

print("The sections of Craigslist are listed below: ")
print(values)

# Create list of towns to include in search

towns = ['eastnc', 'daytona', 'onslow', 'outerbanks', 'wilmington', 'keys', 'miami', 'panamacity', 'pensacola']
townlist =[]

# Create search URLs

sectionChoice = input("What section of craigslist would you like to search? Please enter one of the exact choices above: ").lower()

if sectionChoice in values:
    for town in towns:
        for key, value in sections.items():
            if value == sectionChoice:
                sectionChoiceKey = key
                townlist.append('https://' + town + '.craigslist.org/search/'+ sectionChoiceKey +'?query=' + query)
                print(townlist)
else:
    print("You did not select a valid Craigslist section. Please try again.")
    exit()

# Create Spider

class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["craigslist.org"]
    def start_requests(self):
        urls = townlist
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_info = response.xpath('//p[@class="result-info"]')

        for item in item_info:
            name = item.xpath('a/text()').extract_first()
            price = item.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first()
            url = item.xpath('a/@href').extract_first()

            if int(price.strip("$")) > 100:
                yield{'Title':name, 'Price':price, 'Link':url}