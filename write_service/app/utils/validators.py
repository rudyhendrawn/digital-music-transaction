from fastapi import HTTPException
from app.db.database import database

async def get_album_or_404(album_id: int):
	query = "SELECT * from Album WHERE AlbumId = :AlbumId"
	album = await database.fetch_one(query=query, values={"AlbumId": album_id})

	if album is None:
		raise HTTPException(status_code=404, detail="Album not found")
	return album

async def check_album_exists(title: str, artist_id: int):
	query = "SELECT * from Album WHERE Title = :Title AND ArtistId = :ArtistId"
	album = await database.fetch_one(query=query, values={"Title": title, "ArtistId": artist_id})

	if album:
		raise HTTPException(status_code=400, detail="Album already exists")
	return album