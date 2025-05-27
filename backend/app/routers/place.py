from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.place import (
    delete_place,
    get_all_places,
    get_place,
    post_place,
    update_place,
)
from app.db.db_setup import get_session
from app.models.place import Place, PlaceCreate, PlaceUpdate

router = APIRouter(
    tags=["places"], 
    responses={404: {"description": "No places found, sorry!"}}
)

@router.post("/places/", response_model=Place, status_code=201)
def create(place: PlaceCreate, session: Session = Depends(get_session)) -> Place:
    new_place = Place.model_validate(place)
    return post_place(session, new_place)


@router.get("/places/{place_name}", response_model=Place, status_code=200)
def get_by_name(place_name: str, session: Session = Depends(get_session)) -> Place:
    place = get_place(session, place_name)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place