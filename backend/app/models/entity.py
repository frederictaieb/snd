from typing import TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

# Importer PersonEntityLink directement
from .person import PersonBase, PersonEntityLink 

if TYPE_CHECKING:
    from .person import Person # Garder Person sous TYPE_CHECKING pour la List["Person"]
    # PersonEntityLink peut être importé directement car il est utilisé comme valeur (link_model=PersonEntityLink)
    # et non seulement comme type hint qui pourrait causer une circularité s'il était complexe.

class EntityBase(SQLModel):
    name: str = Field(index=True, unique=True) # Example field
    # Add other fields specific to your entity here

class Entity(EntityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    persons: List["Person"] = Relationship(
        back_populates="entities", 
        link_model=PersonEntityLink, # Utiliser la classe importée directement
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class EntityCreate(EntityBase):
    pass

class EntityUpdate(SQLModel):
    name: str | None = None
    # Add other updatable fields here

# Schema for reading an entity with its persons
class EntityRead(EntityBase):
    id: int

# Schema for reading a person (simplified for nesting)
class PersonReadSimple(SQLModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr # Make sure EmailStr is imported or available if you use this here

class EntityReadWithPersons(EntityRead):
    persons: List["PersonReadSimple"] = [] # Use PersonReadSimple or a similar tailored model

# Schema for reading a person with its entities
class PersonRead(PersonBase):
    id: int

class PersonReadWithEntities(PersonRead):
    entities: List["EntityRead"] = [] # Use EntityRead or a similar tailored model

