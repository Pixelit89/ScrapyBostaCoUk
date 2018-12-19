import scrapy
from ..items import BostaCoUkItem

class Spider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['bosta.co.uk']
    start_urls = ['https://www.bosta.co.uk/plastic-pressure-piping-systems/pvc-pressure-pipe-metric/']

    def parse(self, response):
        next = response.xpath('//div[@title="Next page"]/div[1]/div[1]/a[1]/@href').extract_first()
        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse)
        for url in response.xpath('//a[@title="View"]/@href').extract():
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_items)

    def parse_items(self, response):
        info = BostaCoUkItem()
        image_url = response.xpath('//img[@class="carousel_image"]/@src').extract_first()
        title = response.xpath('//h1/text()').extract_first().strip()
        features = response.xpath('//div[@class="productFeatures"]/text()')
        columns = response.xpath('//tr')[1]
        rows = response.xpath('//tr[@class]')
        features_text = []
        for f in features.extract():
            if f.strip():
                features_text.append(f.strip())
        for row in rows:
            try:
                Colour = features_text[1]
            except IndexError:
                Colour = None
            item = {
                'Image_url': image_url,
                'Title': title,
                'Material': features_text[0],
            }
            for i in range(20):
                i = i + 1
                if i == 1:
                    item.update({columns.xpath('td[1]/text()').extract_first(): row.xpath('td[1]/a/text()').extract_first()})
                else:
                    if columns.xpath('td[%s]/text()' % i).extract_first() == 'Quantity':
                        break
                    elif columns.xpath('td[%s]/text()' % i).extract_first() == None:
                        continue
                    else:
                        item.update({columns.xpath('td[%s]/text()' % i).extract_first(): row.xpath('td[%s]//span[contains(@id, "Price")]/text()' % i).extract_first(default=row.xpath('td[%s]/text()' % i).extract_first(default=row.xpath('td[%s]/div[1]/text()' % i)))})
            yield item
            # yield {
            #
            # columns.xpath('td[1]/text()').extract_first(): row.xpath('td[1]/a/text()').extract_first(),
            # columns.xpath('td[2]/text()').extract_first(): row.xpath('td[2]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[2]/text()').extract_first(default=row.xpath('td[2]/div[1]/text()'))),
            # columns.xpath('td[3]/text()').extract_first(): row.xpath('td[3]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[3]/text()').extract_first(default=row.xpath('td[3]/div[1]/text()'))),
            # columns.xpath('td[4]/text()').extract_first(): row.xpath('td[4]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[4]/text()').extract_first(default=row.xpath('td[4]/div[1]/text()'))),
            # columns.xpath('td[5]/text()').extract_first(): row.xpath('td[5]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[5]/text()').extract_first(default=row.xpath('td[5]/div[1]/text()'))),
            # columns.xpath('td[6]/text()').extract_first(): row.xpath('td[6]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[6]/text()').extract_first(default=row.xpath('td[6]/div[1]/text()'))),
            # columns.xpath('td[7]/text()').extract_first(): row.xpath('td[7]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[7]/text()').extract_first(default=row.xpath('td[7]/div[1]/text()'))),
            # columns.xpath('td[8]/text()').extract_first(): row.xpath('td[8]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[8]/text()').extract_first(default=row.xpath('td[8]/div[1]/text()'))),
            # columns.xpath('td[9]/text()').extract_first(): row.xpath('td[9]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[9]/text()').extract_first(default=row.xpath('td[9]/div[1]/text()'))),
            # columns.xpath('td[10]/text()').extract_first(): row.xpath('td[10]//span[contains(@id, "Price")]/text()').extract_first(default=row.xpath('td[10]/text()').extract_first(default=row.xpath('td[10]/div[1]/text()'))),
            # }
            # info['Image_url'] = image_url
            # info['Title'] = title
            # info['Material'] = features_text[0]
            # try:
            #     info['Colour'] = features_text[1]
            # except IndexError:
            #     info['Colour'] = None
            # info['Item_no'] = row.xpath('td[1]/a/text()').extract_first()
            # info['Size'] = row.xpath('td[@class="gviCnt"][1]/text()').extract_first(),
            # info['Wall_thickness'] = row.xpath('td[@class="gviCnt"][2]/text()').extract_first(),
            # info['Length'] = row.xpath('td[@class="gviCnt"][3]/text()').extract_first(),
            # info['Pressure'] = row.xpath('td[@class="gviCnt"][4]/text()').extract_first(),
            # info['Price'] = row.xpath('td[6]//span[contains(@id, "Price")]/text()').extract_first(),
            # info['UOM'] = row.xpath('td[8]/text()').extract_first(),
            # info['Box_quantity'] = row.xpath('td[9]/text()').extract_first(),
            # info['MSQ'] = row.xpath('td[10]/text()').extract_first(),
            # yield info