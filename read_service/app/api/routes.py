from fastapi import APIRouter, Depends, HTTPException
from app.db.database import database
from app.db.models import Album
from app.utils.cache import cache
from typing import List

import logging

router = APIRouter()

@router.get("/album/{album_id}", response_model=Album)
@cache(expire=60)
async def read_album(album_id: int):
	query = "SELECT * FROM Album WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=query, values={"AlbumId": album_id})
	if album_row:
		# Convert the record to an Album instance
		album = Album(**dict(album_row))
		return album
	else:
		raise HTTPException(status_code=404, detail="Album not found")

@router.get("/album", response_model=List[Album])
@cache(expire=60)
async def read_albums():
	query = "SELECT * FROM Album"
	album_rows = await database.fetch_all(query=query)

	if album_rows:
		# Convert each record into an Album instance
		albums = [Album(**dict(row)) for row in album_rows]

		# Log the number of albums fetched
		logging.info(f"Fetched {len(albums)} albums")

		return albums
	else:
		raise HTTPException(status_code=404, detail="No albums found")
	
	return albums