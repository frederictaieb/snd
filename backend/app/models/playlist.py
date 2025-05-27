from sqlmodel import Field, SQLModel

class PlaylistBase(SQLModel):
   name: str = Field(index=True)
   filename: str  = Field()
   peaksfile: str = Field() 
   count_listen : int = Field()

class Playlist(PlaylistBase, table=True): 
    id: int | None = Field(default=None, primary_key=True)

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(SQLModel):
    name: str | None = None
    filename: str | None = None
    peaksfile: str | None = None
    count_listen: int | None = None