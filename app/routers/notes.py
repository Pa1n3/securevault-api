from fastapi import APIRouter, HTTPException, Depends
from app.schemas import NoteCreate, NoteUpdate
from app.database import execute_query
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/")
def create_note(data: NoteCreate, current_user: dict = Depends(get_current_user)):
    note = execute_query(
        """
        INSERT INTO notes (user_id, title, content, is_private)
        VALUES (%s, %s, %s, %s)
        RETURNING id, user_id, title, content, is_private
        """,
        (current_user["id"], data.title, data.content, data.is_private),
        fetch='one'
    )
    return {"id": note[0], "user_id": note[1], "title": note[2],
            "content": note[3], "is_private": note[4]}


@router.get("/")
def get_my_notes(current_user: dict = Depends(get_current_user)):
    """Get only YOUR notes"""
    notes = execute_query(
        "SELECT id, title, content, is_private FROM notes WHERE user_id = %s",
        (current_user["id"],),
        fetch='all'
    )
    return [{"id": n[0], "title": n[1], "content": n[2], "is_private": n[3]} 
            for n in notes]


@router.get("/{note_id}")
def get_note(note_id: int, current_user: dict = Depends(get_current_user)):
    """
    Get a single note.
    
    ⚠️  IDOR VULNERABILITY LIVES HERE — intentionally.
    Notice: we're fetching by note_id WITHOUT checking user_id.
    Any logged-in user can read any note by changing the ID.
    
    This is what you'll learn to find on real targets.
    After building: try accessing note_id=1 with a different user account.
    """
    note = execute_query(
        "SELECT id, user_id, title, content, is_private FROM notes WHERE id = %s AND user_id = %s",
        (note_id,current_user["id"]),  # ← missing "AND user_id = %s" — intentional bug
        fetch='one'
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"id": note[0], "user_id": note[1], "title": note[2],
            "content": note[3], "is_private": note[4]}


@router.put("/{note_id}")
def update_note(note_id: int, data: NoteUpdate, 
                current_user: dict = Depends(get_current_user)):
    # This one IS secure — checks ownership
    note = execute_query(
        "SELECT id FROM notes WHERE id = %s AND user_id = %s",
        (note_id, current_user["id"]),
        fetch='one'
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or not yours")
    
    execute_query(
        """
        UPDATE notes SET title = COALESCE(%s, title),
                         content = COALESCE(%s, content),
                         is_private = COALESCE(%s, is_private),
                         updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND user_id = %s
        """,
        (data.title, data.content, data.is_private, note_id, current_user["id"])
    )
    
    return {"message": "Note updated"}


@router.delete("/{note_id}")
def delete_note(note_id: int, current_user: dict = Depends(get_current_user)):
    execute_query(
        "DELETE FROM notes WHERE id = %s AND user_id = %s",
        (note_id, current_user["id"])
    )
    return {"message": "Note deleted"}


@router.get("/admin/all")
def get_all_notes(admin: dict = Depends(require_admin)):
    """Admin only — see every note from every user"""
    notes = execute_query(
        "SELECT n.id, u.username, n.title, n.content FROM notes n JOIN users u ON n.user_id = u.id",
        fetch='all'
    )
    return [{"id": n[0], "username": n[1], "title": n[2], "content": n[3]} 
            for n in notes]