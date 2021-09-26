from spider_demo.items import SpiderDemoItem
from spider_demo.settings import db, table_name


class SpiderDemoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, SpiderDemoItem):
            insert_data = dict(item)
            insert_data['product_id#pk'] = insert_data.pop('product_id')
            db.insert_or_update(insert_data, table_name=table_name)
        return item
