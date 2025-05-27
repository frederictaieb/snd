from sqlmodel import Session, select

from app.db.db_setup import engine
from app.models.place import Place, PlaceCreate, PlaceUpdate


def post_place(session: Session, place: PlaceCreate) -> Place:
    db_place = Place.model_validate(place) 
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    return db_place

def get_place(session: Session, place_name: str) -> Place | None:
    query = select(Place).where(Place.name == place_name)
    return session.exec(query).first()


def get_all_places(session: Session) -> list[Place]:
    query = select(Place)
    return list(session.exec(query).all())


def update_place(session: Session, place_name: str, place_update: PlaceUpdate) -> Place | None:
    db_place = get_place(session, place_name)
    if not db_place:
        return None
    
    place_data = place_update.model_dump(exclude_unset=True)
    for key, value in place_data.items():
        setattr(db_place, key, value)
    
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    return db_place


def delete_place(session: Session, place_name: str) -> Place | None:
    place = get_place(session, place_name)
    if place:
        session.delete(place)
        session.commit()
        return place
    return None