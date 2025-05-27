from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .place import Place
    from .playlist import Playlist
    from .entity import Entity

class EventBase(SQLModel):
    name: str = Field(index=True)
    happened_on: datetime = Field(index=True)
    place: Place = Field(foreign_key="place.id")
    playlist: Playlist = Field(foreign_key="playlist.id")
    entity: Entity = Field(foreign_key="entity.id")

class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class EventCreate(EventBase):
    pass

class EventUpdate(SQLModel):
    name: str | None = None
    happened_on: datetime | None = None
    place: Place | None = None
    playlist: Playlist | None = None
    entity: Entity | None = None