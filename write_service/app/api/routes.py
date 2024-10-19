from fastapi import APIRouter, HTTPException, Depends
from app.db.database import database
from app.db.models import AlbumCreate, AlbumUpdate, Album

router = APIRouter()

@router.post("/albums", response_model=Album)
async def create_album(album: AlbumCreate):
	query = "INSERT INTO albums (Title, ArtistId) VALUES (:Title, :ArtisId)"
	values = {"Title": album.Title, "ArtisId": album.ArtisId}
	album_id = await database.execute(query=query, values=values)

	# Fetch the created album
	select_query = "SELECT * FROM albums WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=select_query, values={"AlbumId": album_id})
	if album_row:
		return album_row
	else:
		raise HTTPException(status_code=500, detail="Failed to create album")

@router.put("/albums/{album_id}", response_model=Album)
async def update_album(album_id: int, album: AlbumUpdate):
	update_data = album.dict(exclude_unset=True)
	if not update_data:
		raise HTTPException(status_code=400, detail="No fields to update")
	set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
	update_data["AlbumId"] = album_id
	query = f"UPDATE albums SET {set_clause} WHERE AlbumId = :AlbumId"
	await database.execute(query=query, values=update_data)

	# Fetch the updated album
	select_query = "SELECT * FROM albums WHERE AlbumId = :AlbumId"
	album_row = await database.fetch_one(query=select_query, values={"AlbumId": album_id})
	if album_row:
		return album_row
	else:
		raise HTTPException(status_code=404, detail="Album not found")

@router.delete("/albums/{album_id}")
async def delete_album(album_id: int):
	query = "DELETE FROM albums WHERE AlbumId = :AlbumId"
	result = await database.execute(query=query, values={"AlbumId": album_id})
	if result:
		return {"detail": "Album deleted successfully"}
	else:
		raise HTTPException(status_code=404, detail="Album not found")