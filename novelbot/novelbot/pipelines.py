from scrapy.exceptions import DropItem
import hashlib
import couchdb


couch = couchdb.Server()
db = couch['novel']


class SaveToDBPipeline(object):
    "Save posts to the couchdb"
    def process_item(self, item, spider):
        item_dict = dict(item)
        h = hashlib.sha256()
        h.update(item['body'].encode('utf-8'))
        item_dict['_id'] = h.hexdigest()
        db.save(item_dict)
        return item
