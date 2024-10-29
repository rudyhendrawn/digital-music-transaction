from fastapi import APIRouter, HTTPException, Depends
from app.db.database import database
from app.db.models import AlbumCreate, AlbumUpdate, Album
from app.utils.cache import redis_cache
from app.utils.validators import get_album_or_404, check_album_exists

import logging

router = APIRouter()

@router.post("/album", response_model=Album)
async def create_album(album: AlbumCreate):
	# Check if the album already exists
	exist_album = await check_album_exists(album.Title, album.ArtistId)

	# Insert the album into the database
	query = "INSERT INTO Album (Title, ArtistId) VALUES (:Title, :ArtistId)"
	values = {"Title": album.Title, "ArtistId": album.ArtistId}
	album_id = await database.execute(query=query, values=values)

	# Fetch the created Album
	album_row = await get_album_or_404(album_id)

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

@router.put("/album/{album_id}", response_model=Album)
async def update_album(album_id: int, album: AlbumUpdate):
	# Check if the album exists
	exist_album = await get_album_or_404(album_id)

	# Update the album
	update_data = album.dict(exclude_unset=True)
	if not update_data:
		raise HTTPException(status_code=400, detail="No fields to update")

	set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
	update_data["AlbumId"] = album_id
	query = f"UPDATE Album SET {set_clause} WHERE AlbumId = :AlbumId"
	await database.execute(query=query, values=update_data)

	# Fetch the updated album
	album_row = await get_album_or_404(album_id)
	
	# Convert the record to a dictionary
	album_data = Album(**dict(album_row))

	# Log the album update
	logging.info(f"Album updated: {album_id}")

	# Invalidate the cache
	await redis_cache.invalidate(f"read_album:{album_id}")
	await redis_cache.invalidate("read_albums")
	
	return album_row
	
@router.delete("/album/{album_id}")
async def delete_album(album_id: int):
	# Validate the album exists
	existing_album = await get_album_or_404(album_id)

	# Delete the album from the database
	query = "DELETE FROM Album WHERE AlbumId = :AlbumId"
	result = await database.execute(query=query, values={"AlbumId": album_id})

	if result:
		# Log the album deletion
		logging.info(f"Album deleted: {album_id}")

		# Invalidate the cache
		await redis_cache.invalidate(f"read_album:{album_id}")
		await redis_cache.invalidate("read_albums")
		return {"detail": "Album deleted successfully"}
	else:
		raise HTTPException(status_code=500, detail="Failed to delete album")