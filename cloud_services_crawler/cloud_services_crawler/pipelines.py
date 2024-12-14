# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import scrapy

class CloudServicesPipeline:
    def open_spider(self, spider):
        self.file = open('cloud_services.json', 'w', encoding='utf-8')
        self.file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, scrapy.Item) and 'service_name' in item and 'provider' in item:
            if not self.first_item:
                self.file.write(',\n')
            else:
                self.first_item = False
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
        return item

class ServiceReviewsPipeline:
    def open_spider(self, spider):
        self.file = open('service_reviews.json', 'w', encoding='utf-8')
        self.file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, scrapy.Item) and 'review_text' in item:
            if not self.first_item:
                self.file.write(',\n')
            else:
                self.first_item = False
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
        return item