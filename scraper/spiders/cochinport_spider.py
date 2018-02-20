import scrapy
from scrapy.selector import Selector
from ..items import VesselsItem, MovementItem, PositionItem
import re


class CochinportSpider(scrapy.Spider):
    name = "cochin"

    def start_requests(self):
        urls = [
            'http://cochinport.gov.in/index.php?opt=shipsatport&cat=ev&tab=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # get shipsinport tables
        shipsinport = response.xpath('//table[@class="shipsinport"]').extract()
        table_vessel_position = shipsinport[0]
        table_shipping_movement = shipsinport[1]
        table_expected_vessels = shipsinport[2]

        # table: expected vessels
        vellels_rows = Selector(text=table_expected_vessels).xpath('//tr')

        # extrated table data of each row
        for row in vellels_rows[2:]:
            item = VesselsItem()

            item['date'] = row.xpath('td[1]/text()').extract_first()
            item['ata_eta'] = row.xpath('td[2]/text()').extract_first()
            item['vessel'] = row.xpath('td[3]/text()').extract_first()
            item['cargo'] = row.xpath('td[4]/text()').extract_first()
            item['quantity'] = row.xpath('td[5]/text()').extract_first()
            item['ie'] = row.xpath('td[6]/text()').extract_first()
            item['agent'] = row.xpath('td[7]/text()').extract_first()

            yield item


        # table: shipping movement
        movement_rows = Selector(text=table_shipping_movement).xpath('//tr')

        date = ''
        state = ''

        for row in movement_rows[2:]:
            item = MovementItem()

            # get date
            temp_date = row.xpath('td[@class="hed1"]/text()').extract_first()
            if temp_date is not None:
                date = temp_date
                print (date)
                continue

            # get state: sailing, berthing, shifting, waiting
            temp_state = row.xpath('td[@class="hed"]/text()').extract_first()
            if temp_state is not None:
                state = temp_state
                print (state)

            item['date'] = date
            item['state'] = state
            item['vessel_name'] = row.xpath('td[2]/label/text()').extract_first()
            item['berth_allotted'] = row.xpath('td[3]/label/text()').extract_first()
            item['pilot_boarding_time'] = row.xpath('td[4]/label/text()').extract_first()

            yield item



        # table: vessel position
        position_rows = Selector(text=table_vessel_position).xpath('//tr')

        thead = Selector(text=table_vessel_position).xpath('//th/text()').extract_first()
        # print('thead is: ', thead)
        pattern = r'\d{2}.\d{2}.\d{4}'
        today = re.search(pattern, thead).group()
        # print('today is: ', today)


        for row in position_rows[2:]:
            item = PositionItem()

            item['date'] = today
            item['berth'] = row.xpath('td[1]/label/text()').extract_first()
            item['vessel'] = row.xpath('td[2]/label/text()').extract_first()
            item['ie'] = row.xpath('td[3]/label/text()').extract_first()
            item['fc'] = row.xpath('td[4]/label/text()').extract_first()
            item['date_of_berthing'] = row.xpath('td[5]/label/text()').extract_first()
            item['cargo'] = row.xpath('td[6]/label/text()').extract_first()
            item['quantity'] = row.xpath('td[7]/label/text()').extract_first()
            item['day_s_handling'] = row.xpath('td[8]/label/text()').extract_first()
            item['up_to_date_hanfling'] = row.xpath('td[9]/label/text()').extract_first()
            item['balance'] = row.xpath('td[10]/label/text()').extract_first()
            item['load_or_discharge_port'] = row.xpath('td[11]/label/text()').extract_first()
            item['agent'] = row.xpath('td[12]/label/text()').extract_first()

            yield item

