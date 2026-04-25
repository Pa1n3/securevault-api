import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.database import execute_query
from app.auth import get_current_user

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".txt"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Check extension
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Read content and check size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    
    # Generate safe filename (never trust the original filename)
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(contents)
    
    # Save record to DB
    record = execute_query(
        """
        INSERT INTO files (user_id, filename, filepath, filesize)
        VALUES (%s, %s, %s, %s)
        RETURNING id, filename, filesize
        """,
        (current_user["id"], file.filename, filepath, len(contents)),
        fetch='one'
    )
    
    return {
        "id": record[0],
        "original_name": record[1],
        "size": record[2],
        "saved_as": safe_filename
    }


@router.get("/")
def get_my_files(current_user: dict = Depends(get_current_user)):
    files = execute_query(
        "SELECT id, filename, filesize, uploaded_at FROM files WHERE user_id = %s",
        (current_user["id"],),
        fetch='all'
    )
    return [{"id": f[0], "filename": f[1], "size": f[2], "uploaded": str(f[3])} 
            for f in files]