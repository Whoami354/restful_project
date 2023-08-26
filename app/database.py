from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27000/')
        
async def get_collection(collection: str):
    try:
        api_db = mongo_client["APIDB"]
        collection = api_db[collection]
    except api_db.exceptions.RequestException as e:
        return {"mongo_client error": str(e)}
    except collection.exceptions.RequestException as e:
        return {"collection error": str(e)}
    return collection

def get_database():
    return mongo_client["APIDB"]
