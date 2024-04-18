import datetime as dt
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
from collections import defaultdict

# from pep_parse.models import Pep, Statistic, Base
from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = defaultdict(int)
        # engine = create_engine('sqlite:///sqlite.db')
        # Base.metadata.create_all(engine)
        # self.session = Session(engine)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        # pep = Pep(
        #     number=item['number'],
        #     name=item['name'],
        #     status=item['status'],
        # )

        # self.session.add(pep)
        # self.session.commit()
        return item

    def close_spider(self, spider):
        time = dt.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        with open(
            BASE_DIR / 'results' / ('status_summary_' + time + '.csv'),
            mode='w',
            encoding='utf-8'
        ) as f:
            total = 0
            f.write('Статус,Количество\n')
            for status in self.status_counter:
                # statistic = Statistic(
                #     status=status,
                #     status_count=self.status_counter[status],
                # )
                # self.session.add(statistic)
                # self.session.commit()
                f.write(f'{status},{self.status_counter[status]}\n')
                total += self.status_counter[status]
            f.write(f'Total,{total}\n')
        # statistic = Statistic(
        #     status='Total',
        #     status_count=total,
        # )
        # self.session.add(statistic)
        # self.session.commit()
        # self.session.close()
