import os
import json
import pymongo


def sync_with_db(mongo_uri):
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_default_database()

    cases = json.load(open('data/processed/all_cases.json'))
    for case in cases:
        case['patient'] = int(case['number'])
        db.cases.update_one({
            'number': case['number']
        }, {
            '$set': case,
        }, upsert=True)

    updates = json.load(open('data/processed/all_updates.json'))
    for update in updates:
        for key in update.keys():
            if 'date' not in key:
                update[key] = int(update[key])

        db.updates.update_one({
            'date': update['date']
        }, {
            '$set': update,
        }, upsert=True)


if __name__ == '__main__':
    mongo_uri = os.getenv('MONGO_URI', None)
    sync_with_db(mongo_uri)
