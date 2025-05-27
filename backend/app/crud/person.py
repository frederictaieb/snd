from typing import List
from sqlmodel import Session, select

from app.models.person import Person, PersonCreate, PersonUpdate
from app.models.entity import Entity # Needed for relationship management

def create_person(session: Session, person_create: PersonCreate) -> Person:
    db_person = Person.model_validate(person_create)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person

def get_person(session: Session, person_id: int) -> Person | None:
    return session.get(Person, person_id)

def get_person_by_email(session: Session, email: str) -> Person | None:
    statement = select(Person).where(Person.email == email)
    return session.exec(statement).first()

def get_persons(session: Session, skip: int = 0, limit: int = 100) -> List[Person]:
    statement = select(Person).offset(skip).limit(limit)
    persons = session.exec(statement).all()
    return list(persons)

def update_person(session: Session, person_id: int, person_update: PersonUpdate) -> Person | None:
    db_person = session.get(Person, person_id)
    if not db_person:
        return None
    
    person_data = person_update.model_dump(exclude_unset=True)
    for key, value in person_data.items():
        setattr(db_person, key, value)
    
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person

def delete_person(session: Session, person_id: int) -> Person | None:
    db_person = session.get(Person, person_id)
    if not db_person:
        return None
    session.delete(db_person)
    session.commit()
    return db_person # Or return {"message": "Person deleted successfully"}

def add_entity_to_person(session: Session, person_id: int, entity_id: int) -> Person | None:
    person = session.get(Person, person_id)
    if not person:
        return None
    
    entity = session.get(Entity, entity_id)
    if not entity:
        return None

    if entity not in person.entities:
        person.entities.append(entity)
        session.add(person)
        session.commit()
        session.refresh(person)
    return person

def remove_entity_from_person(session: Session, person_id: int, entity_id: int) -> Person | None:
    person = session.get(Person, person_id)
    if not person:
        return None
    
    entity = session.get(Entity, entity_id)
    if not entity:
        return None

    if entity in person.entities:
        person.entities.remove(entity)
        session.add(person)
        session.commit()
        session.refresh(person)
    return person
