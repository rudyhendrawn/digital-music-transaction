from pydantic import BaseModel, Field

# Pydantic models
class Album(BaseModel):
	AlbumId: int
	Title: str
	ArtistId: int

	class Config:
		orm_mode = False