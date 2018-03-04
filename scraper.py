import scrapy
import pdb
# https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        # https://doc.scrapy.org/en/latest/topics/selectors.html
        # https://help.parsehub.com/hc/en-us/articles/220618167-Using-XPath-to-select-elements
        # http://www.zvon.org/comp/r/tut-XPath_1.html
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 a ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract()[1],
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
                }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        pdb.set_trace()
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        pdb.set_trace()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

# To run scrapy and save results into file
# scrapy runspider scraper.py -o result.json -t json 2> log.log

# CLI run
# scrapy shell https://doc.scrapy.org/en/latest/_static/selectors-sample1.html

