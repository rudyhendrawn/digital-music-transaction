from pydantic import BaseModel, Field
from typing import Optional

# Pydantic models
class AlbumBase(BaseModel):
	Title: Optional[str] = Field(None, max_length=160)
	ArtistId: Optional[int]

class AlbumCreate(AlbumBase):
	Title: str
	ArtistId: int

class AlbumUpdate(AlbumBase):
	pass

class Album(AlbumBase):
	Id: int = Field(..., alias="AlbumId")
	Title: str
	ArtistId: int

	class Config:
		orm_mode = False
		allow_population_by_field_name = True