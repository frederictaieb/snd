from typing import List
from sqlmodel import Session, select

from app.models.entity import Entity, EntityCreate, EntityUpdate
from app.models.person import Person # Needed for relationship management

def create_entity(session: Session, entity_create: EntityCreate) -> Entity:
    db_entity = Entity.model_validate(entity_create)
    session.add(db_entity)
    session.commit()
    session.refresh(db_entity)
    return db_entity

def get_entity(session: Session, entity_id: int) -> Entity | None:
    return session.get(Entity, entity_id)

def get_entity_by_name(session: Session, name: str) -> Entity | None:
    statement = select(Entity).where(Entity.name == name)
    return session.exec(statement).first()

def get_entities(session: Session, skip: int = 0, limit: int = 100) -> List[Entity]:
    statement = select(Entity).offset(skip).limit(limit)
    entities = session.exec(statement).all()
    return list(entities)

def update_entity(session: Session, entity_id: int, entity_update: EntityUpdate) -> Entity | None:
    db_entity = session.get(Entity, entity_id)
    if not db_entity:
        return None
    
    entity_data = entity_update.model_dump(exclude_unset=True)
    for key, value in entity_data.items():
        setattr(db_entity, key, value)
    
    session.add(db_entity)
    session.commit()
    session.refresh(db_entity)
    return db_entity

def delete_entity(session: Session, entity_id: int) -> Entity | None:
    db_entity = session.get(Entity, entity_id)
    if not db_entity:
        return None
    session.delete(db_entity)
    session.commit()
    # After deletion, the object is expired. Return a representation or a success message.
    # For now, returning the object as it was before deletion confirmation might be misleading
    # if it's accessed after this. A simple dict or message is often better.
    # However, to match other patterns, we can return it if the caller expects it.
    # Or simply return True / False or a message.
    # Let's return the object for now, but be mindful it's no longer in DB.
    return db_entity # Or return {"message": "Entity deleted successfully"}

def add_person_to_entity(session: Session, entity_id: int, person_id: int) -> Entity | None:
    entity = session.get(Entity, entity_id)
    if not entity:
        return None # Or raise HTTPException("Entity not found")
    
    person = session.get(Person, person_id)
    if not person:
        return None # Or raise HTTPException("Person not found")

    # Check if person is already linked to avoid duplicates in the relationship list
    # SQLModel/SQLAlchemy handles duplicates in the link table gracefully (won't insert if PK exists)
    # but good to check if you want to avoid appending to Python list unnecessarily.
    if person not in entity.persons:
        entity.persons.append(person)
        session.add(entity)
        session.commit()
        session.refresh(entity)
    return entity

def remove_person_from_entity(session: Session, entity_id: int, person_id: int) -> Entity | None:
    entity = session.get(Entity, entity_id)
    if not entity:
        return None # Or raise HTTPException("Entity not found")
    
    person = session.get(Person, person_id)
    if not person:
        return None # Or raise HTTPException("Person not found")

    if person in entity.persons:
        entity.persons.remove(person)
        session.add(entity)
        session.commit()
        session.refresh(entity)
    return entity 