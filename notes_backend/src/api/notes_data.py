"""Notes Data Storage and Access Layer

Provides in-memory storage for notes and functions for CRUD operations.
To be used as a persistence layer by the FastAPI backend API.
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class Note(BaseModel):
    """Represents a personal note."""
    id: int = Field(..., description="Unique identifier for the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")
    created_at: datetime = Field(..., description="Timestamp the note was created")
    updated_at: datetime = Field(..., description="Timestamp the note was last updated")


# In-memory notes storage as a simple dictionary {id -> Note}
_notes_storage: Dict[int, Note] = {}
_next_id: int = 1

# PUBLIC_INTERFACE
def list_notes() -> List[Note]:
    """Return a list of all notes."""
    return list(_notes_storage.values())

# PUBLIC_INTERFACE
def get_note(note_id: int) -> Optional[Note]:
    """Retrieve a note by its ID."""
    return _notes_storage.get(note_id)

# PUBLIC_INTERFACE
def create_note(title: str, content: str) -> Note:
    """Create a new note with a unique id."""
    global _next_id
    now = datetime.utcnow()
    note = Note(
        id=_next_id,
        title=title,
        content=content,
        created_at=now,
        updated_at=now
    )
    _notes_storage[_next_id] = note
    _next_id += 1
    return note

# PUBLIC_INTERFACE
def update_note(note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
    """Update an existing note. Returns the updated note or None if not found."""
    note = _notes_storage.get(note_id)
    if not note:
        return None
    updated_data = note.dict()
    if title is not None:
        updated_data['title'] = title
    if content is not None:
        updated_data['content'] = content
    updated_data['updated_at'] = datetime.utcnow()
    updated_note = Note(**updated_data)
    _notes_storage[note_id] = updated_note
    return updated_note

# PUBLIC_INTERFACE
def delete_note(note_id: int) -> bool:
    """Delete a note by its ID. Returns True if deleted, False if not found."""
    return _notes_storage.pop(note_id, None) is not None
