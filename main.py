import logging
from fastapi import FastAPI, HTTPException
from models import Passenger
from schemas import PassengerCreate, PassengerResponse
from database import passenger_collection
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Root route to return a simple message
@app.get("/")
async def root():
    return {"message": "Welcome to the Passenger API!"}

# Helper function to convert MongoDB result to dict
def passenger_helper(passenger) -> dict:
    return {
        "id": str(passenger["_id"]),
        "title": passenger["title"],
        "given_name": passenger["given_name"],
        "surname": passenger["surname"],
        "passport_number": passenger.get("passport_number"),
        "date_of_birth": passenger.get("date_of_birth"),
        "date_of_expiration": passenger.get("date_of_expiration"),
        "email": passenger["email"],
        "mobile": passenger["mobile"],
        "emergency_contact": passenger.get("emergency_contact"),
        "organization_name": passenger.get("organization_name"),
        "designation": passenger.get("designation"),
        "frequent_flyer_number": passenger.get("frequent_flyer_number"),
        "recent_route": passenger.get("recent_route"),
        "favourite_carrier": passenger.get("favourite_carrier"),
        "meal_preference": passenger.get("meal_preference"),
        "accessibility": passenger.get("accessibility"),
        "baggage_preference": passenger.get("baggage_preference")
    }

# Endpoint to create a new passenger profile
@app.post("/passenger/create", response_model=PassengerResponse)
async def create_passenger(passenger: PassengerCreate):
    try:
        logging.info("Creating a new passenger...")
        passenger_data = jsonable_encoder(passenger)
        new_passenger = await passenger_collection.insert_one(passenger_data)
        created_passenger = await passenger_collection.find_one({"_id": new_passenger.inserted_id})
        
        if created_passenger is None:
            raise HTTPException(status_code=404, detail="Passenger not found after creation")

        logging.info(f"Passenger created: {created_passenger}")
        return passenger_helper(created_passenger)
    except Exception as e:
        logging.error(f"Error creating passenger: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Function to convert datetime.date to string (ISO format)
def convert_dates_to_string(passenger_data: dict) -> dict:
    if "date_of_birth" in passenger_data and isinstance(passenger_data["date_of_birth"], (datetime.date,)):
        passenger_data["date_of_birth"] = passenger_data["date_of_birth"].isoformat()
    
    if "date_of_expiration" in passenger_data and isinstance(passenger_data["date_of_expiration"], (datetime.date,)):
        passenger_data["date_of_expiration"] = passenger_data["date_of_expiration"].isoformat()
    
    return passenger_data

# Endpoint to get passenger profile by ID
@app.get("/passenger/{id}", response_model=PassengerResponse)
async def get_passenger(id: str):
    try:
        logging.info(f"Fetching passenger with ID: {id}")
        passenger = await passenger_collection.find_one({"_id": ObjectId(id)})
        
        if passenger:
            logging.info(f"Passenger found: {passenger}")
            return passenger_helper(passenger)
        else:
            logging.warning(f"Passenger with ID {id} not found")
            raise HTTPException(status_code=404, detail="Passenger not found")
    except Exception as e:
        logging.error(f"Error fetching passenger with ID {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update passenger profile
@app.put("/passenger/{id}/update", response_model=PassengerResponse)
async def update_passenger(id: str, passenger: PassengerCreate):
    try:
        logging.info(f"Updating passenger with ID: {id}")
        
        # Fetch the existing passenger data from the database
        existing_passenger = await passenger_collection.find_one({"_id": ObjectId(id)})
        if not existing_passenger:
            raise HTTPException(status_code=404, detail="Passenger not found")
        
        # Create a dictionary of the existing data
        existing_passenger_data = passenger_helper(existing_passenger)

        # Get only the updated fields from the request body
        update_data = {k: v for k, v in passenger.dict(exclude_unset=True).items()}

        # Merge the existing data with the new updates (keeping the existing data if not provided in update)
        merged_data = {**existing_passenger_data, **update_data}

        # Handle date conversion before updating
        merged_data = convert_dates_to_string(merged_data)

        # Update the database with the merged data
        update_result = await passenger_collection.update_one({"_id": ObjectId(id)}, {"$set": merged_data})

        if update_result.modified_count == 1:
            updated_passenger = await passenger_collection.find_one({"_id": ObjectId(id)})
            if updated_passenger:
                logging.info(f"Passenger updated: {updated_passenger}")
                return passenger_helper(updated_passenger)

        logging.warning(f"Passenger with ID {id} not found")
        raise HTTPException(status_code=404, detail="Passenger not found")
    except Exception as e:
        logging.error(f"Error updating passenger with ID {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete passenger profile
@app.delete("/passenger/{id}/delete")
async def delete_passenger(id: str):
    try:
        logging.info(f"Deleting passenger with ID: {id}")
        delete_result = await passenger_collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            logging.info(f"Passenger with ID {id} deleted successfully")
            return {"message": "Passenger deleted successfully"}
        
        logging.warning(f"Passenger with ID {id} not found")
        raise HTTPException(status_code=404, detail="Passenger not found")
    except Exception as e:
        logging.error(f"Error deleting passenger with ID {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
