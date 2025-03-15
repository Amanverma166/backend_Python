from sqlalchemy import Date, String, Integer, Column, Boolean
from sqlalchemy.orm import validates
from database import Base

def create_tables():
    Base.metadata.create_all()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    ismale = Column(Boolean, nullable=True)
    Date_of_Birth = Column(Date, nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    current_year = Column(Integer, nullable=True)
    Branch = Column(String(100), nullable=True)
    phone_number = Column(Integer, nullable=True)

    @validates("email")
    def validate_email(self, key, value):
        if value is not None and '@' not in value:
            raise ValueError("Invalid email format")
        return value

    @validates("Branch")
    def validate_branch(self, key, value):
        if value:
            normalized_value = normalize_branch(value)  # Normalize branch name using a helper function
            return normalized_value
        return value

    @validates("phone_number")
    def validate_phone_number(self, key, value):
        if len(str(value)) != 10:
            raise ValueError("Phone number must be 10 digits")
        return value

# Helper function to normalize branch names
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
    raise ValueError("Invalid branch name")
