from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import EmailStr # Pour valider le paramètre email dans la route

from app.db.db_setup import get_session # Assurez-vous que ce chemin est correct
from app.models.person import Person, PersonCreate, PersonUpdate # Modèles de base
# Les schémas de lecture avec relations sont dans entity.py ou person.py selon votre organisation
# Assumons qu'ils sont accessibles ou à définir si besoin pour PersonReadWithEntities
from app.models.entity import PersonRead, PersonReadWithEntities # Si définis dans entity.py
# Si PersonRead/PersonReadWithEntities sont dans person.py, ajustez l'import
# from app.models.person import PersonRead, PersonReadWithEntities 

from app.crud.person import (
    create_person,
    get_person,
    get_person_by_email,
    get_persons,
    update_person,
    delete_person,
    add_entity_to_person,
    remove_entity_from_person,
)

router = APIRouter(
    prefix="/persons",
    tags=["Persons"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_new_person(
    *, 
    session: Session = Depends(get_session), 
    person_in: PersonCreate
) -> Person:
    """
    Create new person.
    """
    # Pourrait vérifier si un email existe déjà si l'email doit être unique et qu'il n'y a pas de contrainte DB
    # db_person_by_email = get_person_by_email(session, email=person_in.email)
    # if db_person_by_email:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return create_person(session=session, person_create=person_in)

@router.get("/", response_model=List[PersonRead])
def read_all_persons(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
) -> List[Person]:
    """
    Retrieve all persons.
    """
    return get_persons(session=session, skip=skip, limit=limit)

@router.get("/{person_id}", response_model=PersonReadWithEntities)
def read_person_by_id(
    person_id: int, 
    session: Session = Depends(get_session)
) -> Person:
    """
    Get person by ID, with their associated entities.
    """
    db_person = get_person(session=session, person_id=person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.get("/by_email/{email}", response_model=PersonReadWithEntities)
def read_person_by_email_route(
    email: EmailStr, # Utilise EmailStr pour la validation du format de l'email
    session: Session = Depends(get_session)
) -> Person:
    """
    Get person by email, with their associated entities.
    """
    db_person = get_person_by_email(session=session, email=email)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found with this email")
    return db_person

@router.patch("/{person_id}", response_model=PersonRead)
def update_existing_person(
    person_id: int, 
    person_in: PersonUpdate, 
    session: Session = Depends(get_session)
) -> Person:
    """
    Update a person.
    """
    db_person = update_person(session=session, person_id=person_id, person_update=person_in)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/{person_id}", status_code=status.HTTP_200_OK)
def delete_existing_person(
    person_id: int, 
    session: Session = Depends(get_session)
) -> dict:
    """
    Delete a person.
    """
    deleted = delete_person(session=session, person_id=person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted successfully"}

@router.post("/{person_id}/entities/{entity_id}", response_model=PersonReadWithEntities)
def link_entity_to_person(
    person_id: int,
    entity_id: int,
    session: Session = Depends(get_session)
) -> Person:
    """
    Link an entity to a person.
    """
    person = add_entity_to_person(session=session, person_id=person_id, entity_id=entity_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person or Entity not found, or already linked")
    return person

@router.delete("/{person_id}/entities/{entity_id}", response_model=PersonReadWithEntities)
def unlink_entity_from_person(
    person_id: int,
    entity_id: int,
    session: Session = Depends(get_session)
) -> Person:
    """
    Unlink an entity from a person.
    """
    person = remove_entity_from_person(session=session, person_id=person_id, entity_id=entity_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person or Entity not found, or not linked")
    return person 