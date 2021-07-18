import scrapy

class Spider12(scrapy.Spider):
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'FEED_FORMAT': 'json',
                       'FEED_URI': 'result.json',
                       'DEPTH_LIMIT': 2,
                       'FEED_EXPORT_ENCODING': 'utf-8'
                       }
    start_urls = [
        'https://www.pagina12.com.ar/secciones/el-pais',
        'https://www.pagina12.com.ar/secciones/economia',
        'https://www.pagina12.com.ar/secciones/sociedad',
        'https://www.pagina12.com.ar/secciones/cultura-y-espectaculos',
        'https://www.pagina12.com.ar/secciones/deportes'
    ]

    def parse(self, response):
        # Process featured article
        featured_note = response.xpath('//article[@class="top-content"]//h2/a/@href').get()
        if featured_note is not None:
            yield response.follow(featured_note, callback=self.parse_note)
        # Notes list
        notes = response.xpath('//div[@class="articles-list"]//h4/a/@href').getall()
        for note in notes:
            yield response.follow(note, callback=self.parse_note)
        # Next page
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_note(self, response):
        title = response.xpath('//article[@class="article-full section"]//h1/text()').get()
        body = response.xpath('//div[@class="article-main-content article-text "]//text()').getall()
        if body is not None:
            body = ' '.join(body)

        yield {'url': response.url,
               'title': title,
               'body': body}

from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(Spider12)
process.start()
