import scrapy
from ..items import WhiskyscraperItem
from scrapy.loader import ItemLoader

class WhiskySpider(scrapy.Spider):
    name = 'whisky'
    allowed_domains = ['whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for product in response.xpath('//*[@class="product-item-info"]'):
            l = ItemLoader(WhiskyscraperItem(), selector=product)
            l.add_css('name','a.product-item-link::text')
            l.add_css('price','span.price::text')
            l.add_css('link','.product-item-link::attr(href)')
            yield l.load_item()
            #handling pagination
        next_page = response.css('a.action.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)