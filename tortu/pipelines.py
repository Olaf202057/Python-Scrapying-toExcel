# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from idna import unicode
from scrapy.exporters import CsvItemExporter


class TortuPipeline:

    def __init__(self):
        self.file = open("./path/data.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.fields_to_export = ['Account Owner', 'Account Owner ID', 'Account Name', 'Phone', 'Account Site', 'Fax', 'Parent Account',  'Parent Account ID', 'Account Number', 'Account Type', 'Industry', 'Annual Revenue', 'Created By', 'Created by ID', 'Modified By', 'Modified by ID', 'Created Time', 'Modified Time', 'Billing Street', 'Billing City', 'Billing State', 'Billing Code', 'Billing Country', 'Description', 'Last Activity Time', 'Layout', 'Layout ID', 'Tag', 'Water System No', 'Website URL', 'Principal Country Served']
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
