from sqlmodel import Session, select

from app.db.db_setup import engine
from app.models.music import Music, MusicCreate, MusicUpdate


def post_music(session: Session, music: MusicCreate) -> Music:
    db_music = Music.model_validate(music) 
    session.add(db_music)
    session.commit()
    session.refresh(db_music)
    return db_music

def get_music(session: Session, music_name: str) -> Music | None:
    query = select(Music).where(Music.name == music_name)
    return session.exec(query).first()


def get_all_musics(session: Session) -> list[Music]:
    query = select(Music)
    return list(session.exec(query).all())


def update_music(session: Session, music_name: str, music_update: MusicUpdate) -> Music | None:
    db_music = get_music(session, music_name)
    if not db_music:
        return None
    
    music_data = music_update.model_dump(exclude_unset=True)
    for key, value in music_data.items():
        setattr(db_music, key, value)
    
    session.add(db_music)
    session.commit()
    session.refresh(db_music)
    return db_music


def delete_music(session: Session, music_name: str) -> Music | None:
    music = get_music(session, music_name)
    if music:
        session.delete(music)
        session.commit()
        return music
    return None