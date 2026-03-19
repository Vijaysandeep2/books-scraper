import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        "FEEDS": {
            "books_data.json": {"format": "json", "overwrite": True},
            "books_data.csv": {"format": "csv", "overwrite": True},
        },
        "DOWNLOAD_DELAY": 1,
        "ROBOTSTXT_OBEY": True,
    }

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "rating": book.css("p.star-rating::attr(class)").get().split()[-1],
                "availability": book.css("p.availability::text").getall()[-1].strip(),
                "url": response.urljoin(book.css("h3 a::attr(href)").get()),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
