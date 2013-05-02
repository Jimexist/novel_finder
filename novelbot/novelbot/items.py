from scrapy.item import Item, Field


class Post(Item):
    book_title = Field()
    chapter_title = Field()
    author = Field()
    body = Field()
