from typing import TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from .entity import Entity

# Association Table for Person <-> Entity
class PersonEntityLink(SQLModel, table=True):
    person_id: int | None = Field(
        default=None, primary_key=True, foreign_key="person.id"
    )
    entity_id: int | None = Field(
        default=None, primary_key=True, foreign_key="entity.id"
    )
    # You can add extra data to the relationship here if needed
    # For example: role_in_entity: str | None = None


class PersonBase(SQLModel):
    firstname: str = Field(index=True)
    lastname: str = Field(index=True)
    email: EmailStr = Field(index=True)
    # entity_id: int | None = Field(default=None, foreign_key="entity.id", index=True)

class Person(PersonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # entity: "Entity" | None = Relationship(back_populates="persons")

    entities: List["Entity"] = Relationship(
        back_populates="persons", 
        link_model=PersonEntityLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class PersonCreate(PersonBase):
    # For creating a person, you might later want to accept a list of existing entity IDs
    # to link them immediately, but the base model doesn't need to change for the relationship itself.
    pass

class PersonUpdate(SQLModel):  # Tous les champs sont optionnels pour une mise à jour
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    # entity_id: int | None = None
    # Updating relationships (adding/removing entities) is usually handled by
    # modifying the list on the Person object and committing, or through dedicated endpoints.

