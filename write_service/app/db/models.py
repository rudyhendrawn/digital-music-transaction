from pydantic import BaseModel, Field
from typing import Optional

# Pydantic models
class AlbumBase(BaseModel):
	Title: Optional[str] = Field(None, max_length=160)
	ArtistId: Optional[int]

class AlbumCreate(AlbumBase):
	Title: str
	ArtisId: int

class AlbumUpdate(AlbumBase):
	pass

class Album(AlbumBase):
	Id: int

	class Config:
		orm_mode = False