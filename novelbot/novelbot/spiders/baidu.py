#coding=utf-8
import urlparse

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from novelbot.items import Post


class BaiduSpider(CrawlSpider):
    name = "baidu"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        # Start crawl from the novel index
        "http://tieba.baidu.com/f/fdir?fd=%CE%C4%D1%A7&sd=%C6%E6%BB%C3%A1%A4%D0%FE%BB%C3%D0%A1%CB%B5",
    ]

    def parse_post(self, response):
        "Process post page"
        hxs = HtmlXPathSelector(response)

        posts = hxs.select('//*[@id="j_p_postlist"]/div')
        post_contents = []
        post_author = None

        for post in posts:
            author = post.select('.//a[contains(@class, "p_author_name")]/text()').extract() or post.select('.//div[@class="d_author_anonym"]/text()').extract() 
            author = author[0]
            # Ingore posts by posters other than the OP
            if post_author is None or author == post_author:
                if post_author is None:
                    post_author = author
                content = '\n'.join(post.select('.//div[contains(@class, "j_d_post_content")]/text()').extract())
                post_contents.append(content)
        if post_contents and post_author:
            item = Post()
            item['book_title'] = hxs.select('//*[@id="wd1"]/attribute::value').extract()[0]
            item['chapter_title'] = hxs.select('//h1[@class="core_title_txt"]/text()').extract()[0]
            item['author'] = post_author
            item['body'] = '\n'.join(post_contents)
            return item

    def parse_novel(self, response):
        "Process post index page"
        hxs = HtmlXPathSelector(response)
        threads = hxs.select('//*[@id="thread_list"]/li')

        for thread in threads:
            title = thread.select('.//div[contains(@class,"threadlist_title")]/a/text()').extract()[0]

            # Only crawl posts with specific words in title
            if u'转载' in title or u'连载' in title or u'更新' in title:
                for url in thread.select('.//div[contains(@class,"threadlist_title")]/a/@href').extract():
                    yield Request(urlparse.urljoin('http://tieba.baidu.com/', url), callback=self.parse_post)

        pages = hxs.select('//*[@id="frs_list_pager"]/a')

        for page in pages:
            for url in page.select('@href').extract():
                yield Request(urlparse.urljoin('http://tieba.baidu.com/', url), callback=self.parse_novel)

    def parse(self, response):
        "Process novel index page"
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            if url.startswith('http://tieba.baidu.com/f?kw='):
                novel_url = url.replace('http://tieba.baidu.com/f?kw=', 'http://tieba.baidu.com/f/good?kw=')
                yield Request(novel_url, callback=self.parse_novel)
