from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Schema used when creating a passenger
class PassengerCreate(BaseModel):
    title: str
    given_name: str
    surname: str
    passport_number: Optional[str]
    date_of_birth: Optional[date]
    date_of_expiration: Optional[date]
    email: EmailStr
    mobile: str
    emergency_contact: Optional[str]
    organization_name: Optional[str]
    designation: Optional[str]
    frequent_flyer_number: Optional[str]
    recent_route: Optional[str]
    favourite_carrier: Optional[str]
    meal_preference: Optional[str]
    accessibility: Optional[str]
    baggage_preference: Optional[str]
    
# Schema for response
class PassengerResponse(PassengerCreate):
    id: str
