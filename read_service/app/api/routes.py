from fastapi import APIRouter, Depends, HTTPException
from app.db.database import database
from app.db.models import Album
from app.utils.cache import cache
from typing import List

router = APIRouter()

@router.get("/albums/{album_id}", response_model=Album)
@cache(expire=60)
async def read_album(album_id: int):
	query = "SELECT * FROM albums WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=query, values={"AlbumId": album_id})
	if album_row:
		return album_row
	else:
		raise HTTPException(status_code=404, detail="Album not found")

@router.get("/albums", response_model=List[Album])
@cache(expire=60)
async def read_albums():
	query = "SELECT * FROM albums"
	albums = await database.fetch_all(query=query, values={"Title": f"%{title}%"})
	return albums