from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

class CrwalinsSpider(CrawlSpider):
    name = "crwalspider"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    book_count = 0
    max_books = 100

    rules = (
        Rule(LinkExtractor(allow=("catalogue/category",))),
        Rule(LinkExtractor(allow=("catalogue", "category")), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        if self.book_count >= self.max_books:
            raise CloseSpider("Reached Maximum Limit of 100 books")
        
        self.book_count += 1

        yield {
            "sr.no": self.book_count,
            "Title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "Availability": response.css(".availability::text")[1].get().strip()
        }
