import pymongo
import certifi


con_str = "mongodb+srv://mcostanza14:Jackson9625!@cluster0.afqjf.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("TileStore2")
