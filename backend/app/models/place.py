from sqlmodel import Field, SQLModel

class PlaceBase(SQLModel):
    name: str = Field(index=True)
    address: str = Field()
    zip_code: int = Field()
    city: str = Field(index=True)
    country: str = Field(index=True)

class Place(PlaceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(SQLModel):  # Tous les champs sont optionnels pour une mise à jour
    name: str | None = None
    address: str | None = None
    zip_code: int | None = None
    city: str | None = None
    country: str | None = None
