import csv
import datetime as dt
from collections import defaultdict

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = defaultdict(int)
        self.status_counter_dict = defaultdict(dict)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        self.status_counter_dict[item['status']] = {
            'Статус': item['status'],
            'Количество': self.status_counter[item['status']]
        }
        return item

    def close_spider(self, spider):
        time = dt.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        self.status_counter_dict['Total'] = {
            'Статус': 'Total',
            'Количество': sum(self.status_counter.values()),
        }
        csvfile = open(
            BASE_DIR / 'results' / ('status_summary_' + time + '.csv'),
            mode='w',
            newline='',
            encoding='utf-8'
        )
        writer = csv.DictWriter(
            csvfile, fieldnames=['Статус', 'Количество']
        )
        writer.writeheader()
        writer.writerows(self.status_counter_dict.values())
