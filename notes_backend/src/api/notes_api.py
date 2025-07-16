from fastapi import APIRouter, HTTPException, status
from typing import List
from src.api.notes_data import (
    Note,
    list_notes,
    get_note,
    create_note,
    update_note,
    delete_note,
)
from pydantic import BaseModel, Field

# Request models for note creation and update
class NoteCreateRequest(BaseModel):
    """Model for creating a note"""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")

class NoteUpdateRequest(BaseModel):
    """Model for updating a note"""
    title: str = Field(None, description="Updated title of the note")
    content: str = Field(None, description="Updated content of the note")

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    responses={404: {"description": "Not found"}},
)

# PUBLIC_INTERFACE
@router.get("/", response_model=List[Note], summary="List all notes", description="Returns a list of all notes stored in the system.")
async def read_notes():
    """
    Retrieve a list of all notes.
    Returns:
        List[Note]: List of all notes.
    """
    return list_notes()

# PUBLIC_INTERFACE
@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED, summary="Create a new note", description="Creates a new note with a title and content.")
async def create_new_note(note: NoteCreateRequest):
    """
    Create a new note.
    Parameters:
        note (NoteCreateRequest): Request body with title and content.
    Returns:
        Note: The created note.
    """
    new_note = create_note(title=note.title, content=note.content)
    return new_note

# PUBLIC_INTERFACE
@router.get("/{note_id}", response_model=Note, summary="Get a note by ID", description="Retrieve a note by its unique ID.")
async def get_note_by_id(note_id: int):
    """
    Retrieve a single note by its ID.
    Parameters:
        note_id (int): ID of the note.
    Returns:
        Note: The requested note.
    """
    note = get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.put("/{note_id}", response_model=Note, summary="Update a note", description="Update the title or content of an existing note.")
async def update_note_by_id(note_id: int, note_update: NoteUpdateRequest):
    """
    Update an existing note.
    Parameters:
        note_id (int): ID of the note to update.
        note_update (NoteUpdateRequest): Request body with updated fields.
    Returns:
        Note: The updated note.
    """
    note = update_note(note_id, title=note_update.title, content=note_update.content)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.delete("/{note_id}", response_model=dict, summary="Delete a note", description="Delete a note by its ID.")
async def delete_note_by_id(note_id: int):
    """
    Delete a note by its ID.
    Parameters:
        note_id (int): ID of the note to delete.
    Returns:
        dict: Result of deletion.
    """
    deleted = delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}
