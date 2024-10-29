from fastapi import APIRouter, HTTPException, Depends
from app.db.database import database
from app.db.models import AlbumCreate, AlbumUpdate, Album
from app.utils.cache import redis_cache

import logging

router = APIRouter()

@router.post("/album", response_model=Album)
async def create_album(album: AlbumCreate):
	query = "INSERT INTO Album (Title, ArtistId) VALUES (:Title, :ArtistId)"
	values = {"Title": album.Title, "ArtistId": album.ArtistId}
	album_id = await database.execute(query=query, values=values)

	# Fetch the created Album
	select_query = "SELECT * FROM Album WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=select_query, values={"AlbumId": album_id})

	if album_row:
		# Convert the record to a dictionary
		album_dict = dict(album_row)

		# Create an Album instance
		album_data = Album(**album_dict)

		# Log the album creation
		logging.info(f"Album created: {album_id}")

		# Invalidate the cache
		await redis_cache.invalidate(f"read_album:{album_id}")
		await redis_cache.invalidate("read_albums")
		return album_row
	else:
		raise HTTPException(status_code=500, detail="Failed to create album")

@router.put("/album/{album_id}", response_model=Album)
async def update_album(album_id: int, album: AlbumUpdate):
	update_data = album.dict(exclude_unset=True)

	if not update_data:
		raise HTTPException(status_code=400, detail="No fields to update")

	set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
	update_data["AlbumId"] = album_id
	query = f"UPDATE Album SET {set_clause} WHERE AlbumId = :AlbumId"
	await database.execute(query=query, values=update_data)

	# Fetch the updated album
	select_query = "SELECT * FROM Album WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=select_query, values={"AlbumId": album_id})
	
	if album_row:
		# Convert the record to a dictionary
		album_data = Album(**dict(album_row))

		# Log the album update
		logging.info(f"Album updated: {album_id}")

		# Invalidate the cache
		await redis_cache.invalidate(f"read_album:{album_id}")
		await redis_cache.invalidate("read_albums")
		return album_row
	else:
		raise HTTPException(status_code=404, detail="Album not found")

@router.delete("/album/{album_id}")
async def delete_album(album_id: int):
	query = "DELETE FROM Album WHERE AlbumId = :AlbumId"
	result = await database.execute(query=query, values={"AlbumId": album_id})
	
	if result:
		album_data = dict(result)

		# Log the album deletion
		logging.info(f"Album deleted: {album_id}")

		# Invalidate the cache
		await redis_cache.invalidate(f"read_album:{album_id}")
		await redis_cache.invalidate("read_albums")
		return {"detail": "Album deleted successfully"}
	else:
		raise HTTPException(status_code=404, detail="Album not found")