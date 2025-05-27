from sqlmodel import Field, SQLModel, Relationship
from datetime import timedelta
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .music import Music
    from .playlist import Playlist


class TrackBase(SQLModel):
    music_id: int | None = Field(default=None, foreign_key="music.id", index=True)
    playlist_id: int | None = Field(default=None, foreign_key="playlist.id", index=True)
    start_time: timedelta = Field(default=timedelta(timedelta(0)))
    end_time: timedelta | None = None

class Track(TrackBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    music: "Music" | None = Relationship(back_populates="playlist_tracks")
    playlist: "Playlist" | None = Relationship(back_populates="tracks")

class TrackCreate(TrackBase):
    pass

class TrackUpdate(SQLModel):
    music_id: int | None = None
    playlist_id: int | None = None
    start_time: timedelta | None = None
    end_time: timedelta | None = None

class TrackRead(TrackBase):
    id: int

class MusicReadInner(SQLModel):
    id: int
    title: str

class PlaylistReadInner(SQLModel):
    id: int
    name: str

class TrackReadWithDetails(TrackRead):
    music: MusicReadInner | None = None
    playlist: PlaylistReadInner | None = None