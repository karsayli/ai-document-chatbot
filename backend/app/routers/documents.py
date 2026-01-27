from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

from app.models.schemas import UploadResponse
from app.services.document_processor import get_document_processor

router = APIRouter()

ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    upload_path = None
    try:
        # Save uploaded file temporarily (in backend/uploads directory)
        upload_path = Path("uploads") / file.filename
        upload_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the document
        processor = get_document_processor()
        document_id = processor.process_document(upload_path, file.filename)
        
        # Optionally delete the temporary file after processing
        # upload_path.unlink()
        
        return UploadResponse(
            message="Document uploaded and processed successfully",
            document_id=document_id,
            filename=file.filename
        )
    except Exception as e:
        # Clean up on error
        if upload_path and upload_path.exists():
            try:
                upload_path.unlink()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/list")
async def list_documents():
    """List all processed documents"""
    try:
        # Get unique documents from collection metadata
        processor = get_document_processor()
        collection = processor.collection
        # This is simplified - in production, maintain a separate document registry
        return {"documents": [], "message": "Document listing not fully implemented in MVP"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

