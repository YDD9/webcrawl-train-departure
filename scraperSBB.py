# -*- coding: UTF-8 -*-
import scrapy
import pdb
import time

# https://www.codementor.io/mgalarny/using-scrapy-to-build-your-own-dataset-cz24hsbp5

class BadenDeparture(scrapy.Spider):
    name = "Badendeparture"
    start_urls = ['http://fahrplan.sbb.ch/bin/stboard.exe/fn?ld=std5.a&input=8503504&REQTrain_name=&boardType=dep&time=08:00&maxJourneys=10&dateBegin=21.02.18&dateEnd=08.12.18&selectDate=today&productsFilter=1111110111&start=yes']

    def parse(self, response):
        # pdb.set_trace()
        SET_SELECTOR = 'tr[class*=zebra]'
        for oneTrain in response.css(SET_SELECTOR):
            # from scrapy.utils.response import open_in_browser
            # open_in_browser(response)

            # from scrapy.shell import inspect_response
            # inspect_response(response, self)

            TIME = 'td[class=time] span::text'
            NUMBER = './/td[contains(@class,journey)]/a/span/text()'
            NEXT_STOP = './/td[contains(@class,result)]/span/a/text()'
            PLATFORM = 'td[class=platform] ::text'
            # if '08:00' < oneTrain.css(TIME).extract_first() < '10:00':
            #     return
            yield {
                'time': oneTrain.css(TIME).extract_first(),
                'number': oneTrain.xpath(NUMBER).extract_first(),
                'next stop': oneTrain.xpath(NEXT_STOP).extract_first(),
                'platform': oneTrain.css(PLATFORM).extract_first().replace('\n', ''),
                }
        # All strings must be XML compatible: Unicode u'\u0020' or ASCII, no NULL bytes or control characters
        # http://www.fileformat.info/info/unicode/char/e9/index.htm

        # contains https://stackoverflow.com/questions/39969770/scrapy-xpath-with-text-contains

        # CONTAINS only evaluate one node, a sentence needs evaluating with logical AND as well
        # as UNICODE for special char:
        # NEXT_PAGE_SELECTOR = '//a[text()[contains(.,"Further") and contains(.,"connections")]]/@href'
        # NEXT_PAGE_SELECTOR = '//a[text()[contains(.,"Autre") and contains(., "itin\u00E9raires")]]/@href'
        NEXT_PAGE_SELECTOR = '//a[text()[contains(.,"Autre")]]/@href'
        time.sleep(2)  # without stop netx_page does not work
        pdb.set_trace()
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

# To run scrapy open shell terminal
# save results into a file: -o FILENAME
# specify a format: -t json
# Redirect results and logs to a file: 2 > LOGFILENAME
# scrapy runspider scraperSBB.py -o resultSBB.json -t json 2> logSBB.log

# Interactive debug
# scrapy shell 'http://fahrplan.sbb.ch/bin/stboard.exe/fn?ld=std5.a&input=8503504&REQTrain_name=&boardType=dep&time=08:00&maxJourneys=20&dateBegin=21.02.18&dateEnd=08.12.18&selectDate=today&productsFilter=1111110111&start=yes' --nolog