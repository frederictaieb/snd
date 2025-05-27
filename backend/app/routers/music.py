from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.music import (
    delete_music,
    get_all_musics,
    get_music,
    post_music,
    update_music,
)
from app.db.db_setup import get_session
from app.models.music import Music, MusicCreate, MusicUpdate

router = APIRouter(
    tags=["musics"], 
    responses={404: {"description": "No musics found, sorry!"}}
)

@router.post("/musics/", response_model=Music, status_code=201)
def create(music: MusicCreate, session: Session = Depends(get_session)) -> Music:
    new_music = Music.model_validate(music)
    return post_music(session, new_music)


@router.get("/musics/{music_name}", response_model=Music, status_code=200)
def get_by_name(music_name: str, session: Session = Depends(get_session)) -> Music:
    music = get_music(session, music_name)
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    return music