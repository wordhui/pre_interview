import scrapy


class SpiderDemoItem(scrapy.Item):
    product_id = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    sales = scrapy.Field()
    from_word = scrapy.Field()
