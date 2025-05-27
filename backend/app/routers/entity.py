from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.db_setup import get_session # Assurez-vous que ce chemin est correct
from app.models.entity import (
    Entity, 
    EntityCreate, 
    EntityUpdate, 
    EntityRead, 
    EntityReadWithPersons
)
# Importer les schémas de Person si nécessaire pour les types de réponse ou de requête
# from app.models.person import PersonRead

from app.crud.entity import (
    create_entity,
    get_entity,
    get_entity_by_name,
    get_entities,
    update_entity,
    delete_entity,
    add_person_to_entity,
    remove_person_from_entity,
)

router = APIRouter(
    prefix="/entities", # Préfixe pour toutes les routes de ce routeur
    tags=["Entities"], # Tag pour la documentation OpenAPI (Swagger UI)
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=EntityRead, status_code=status.HTTP_201_CREATED)
def create_new_entity(
    *, 
    session: Session = Depends(get_session), 
    entity_in: EntityCreate
) -> Entity:
    """
    Create new entity.
    """
    return create_entity(session=session, entity_create=entity_in)

@router.get("/", response_model=List[EntityRead])
def read_all_entities(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
) -> List[Entity]:
    """
    Retrieve all entities.
    """
    return get_entities(session=session, skip=skip, limit=limit)

@router.get("/{entity_id}", response_model=EntityReadWithPersons)
def read_entity_by_id(
    entity_id: int, 
    session: Session = Depends(get_session)
) -> Entity:
    """
    Get entity by ID, with its associated persons.
    """
    db_entity = get_entity(session=session, entity_id=entity_id)
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity

@router.get("/by_name/{entity_name}", response_model=EntityReadWithPersons)
def read_entity_by_name_route(
    entity_name: str, 
    session: Session = Depends(get_session)
) -> Entity:
    """
    Get entity by name, with its associated persons.
    """
    db_entity = get_entity_by_name(session=session, name=entity_name)
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity

@router.patch("/{entity_id}", response_model=EntityRead)
def update_existing_entity(
    entity_id: int, 
    entity_in: EntityUpdate, 
    session: Session = Depends(get_session)
) -> Entity:
    """
    Update an entity.
    """
    db_entity = update_entity(session=session, entity_id=entity_id, entity_update=entity_in)
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity

@router.delete("/{entity_id}", status_code=status.HTTP_200_OK)
def delete_existing_entity(
    entity_id: int, 
    session: Session = Depends(get_session)
) -> dict: # Retourne un message de confirmation
    """
    Delete an entity.
    """
    deleted = delete_entity(session=session, entity_id=entity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"message": "Entity deleted successfully"}

@router.post("/{entity_id}/persons/{person_id}", response_model=EntityReadWithPersons)
def link_person_to_entity(
    entity_id: int,
    person_id: int,
    session: Session = Depends(get_session)
) -> Entity:
    """
    Link a person to an entity.
    """
    entity = add_person_to_entity(session=session, entity_id=entity_id, person_id=person_id)
    if not entity:
        # Le CRUD devrait être plus précis, mais pour l'instant, on suppose que l'un ou l'autre n'a pas été trouvé
        raise HTTPException(status_code=404, detail="Entity or Person not found, or already linked")
    return entity

@router.delete("/{entity_id}/persons/{person_id}", response_model=EntityReadWithPersons)
def unlink_person_from_entity(
    entity_id: int,
    person_id: int,
    session: Session = Depends(get_session)
) -> Entity:
    """
    Unlink a person from an entity.
    """
    entity = remove_person_from_entity(session=session, entity_id=entity_id, person_id=person_id)
    if not entity:
         # Le CRUD devrait être plus précis
        raise HTTPException(status_code=404, detail="Entity or Person not found, or not linked")
    return entity 