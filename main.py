from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, validator
from datetime import date
from database import SessionLocal
import models

app = FastAPI()

# Create a session to connect to the database
db = SessionLocal()

# Function to normalize the branch name
def normalize_branch(branch: str) -> str:
    valid_branches = {
        "Computer Science": ["CSE", "Computer Science", "computer science", "cs"],
        "Electrical Engineering": ["EEE", "Electrical Engineering", "ee"],
        "Mechanical Engineering": ["ME", "Mechanical Engineering", "me"],
        "Civil Engineering": ["CE", "Civil Engineering", "ce"]
    }
    for standard_branch, variations in valid_branches.items():
        if branch.strip().lower() in [v.lower() for v in variations]:
            return standard_branch
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid branch name")

class Person(BaseModel):
    id: int
    firstname: str
    lastname: str
    ismale: bool
    Date_of_Birth: date
    email: str
    address: str
    current_year: int
    Branch: str
    phone_number: int

    @validator("Branch")
    def validate_branch(cls, value):
        return normalize_branch(value)

    @validator("phone_number")
    def validate_phone_number(cls, value):
        # Ensure phone number is exactly 10 digits
        if len(str(value)) != 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number must be 10 digits.")
        return value

@app.get("/", response_model=list[Person], status_code=status.HTTP_200_OK)
def get_all_persons():
    return db.query(models.Person).all()

@app.post("/addperson", response_model=Person, status_code=status.HTTP_201_CREATED)
def add_person(person: Person):
    # Check if person already exists
    find_person = db.query(models.Person).filter(models.Person.id == person.id).first()
    if find_person is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this ID already exists")
    
    # Add new person
    new_person = models.Person(
        id=person.id,
        firstname=person.firstname,
        lastname=person.lastname,
        ismale=person.ismale,
        Date_of_Birth=person.Date_of_Birth,
        email=person.email,
        address=person.address,
        current_year=person.current_year,
        Branch=person.Branch,
        phone_number=person.phone_number
    )
    
    db.add(new_person)
    db.commit()  # Commit changes to the database
    db.refresh(new_person)  # Refresh the instance to get the updated values from the DB
    return new_person

@app.put("/update_person/{person_id}", response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def update_person(person_id: int, person: Person):
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    
    if not find_person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    
    # Update fields
    find_person.firstname = person.firstname
    find_person.lastname = person.lastname
    find_person.ismale = person.ismale
    find_person.Date_of_Birth = person.Date_of_Birth
    find_person.email = person.email
    find_person.address = person.address
    find_person.current_year = person.current_year
    find_person.Branch = person.Branch
    find_person.phone_number = person.phone_number
    
    db.commit()  # Commit changes to the database
    db.refresh(find_person)  # Refresh the instance to get the updated values from the DB
    return find_person
