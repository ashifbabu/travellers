from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()



# MongoDB Connection String
MONGO_DETAILS = os.getenv("MONGO_URL")



client = AsyncIOMotorClient(MONGO_DETAILS)

# Database and Collection setup
database = client.passenger_db
passenger_collection = database.get_collection("passenger_collection")
