from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date

# Passenger Base Model
class Passenger(BaseModel):
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

    class Config:
        orm_mode = True
