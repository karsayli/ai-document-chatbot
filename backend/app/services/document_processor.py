import os
import uuid
import re
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

# PDF Extraction
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("Warning: PyMuPDF (fitz) not found. Please install pymupdf.")
    # Fallback to PyPDF2 if needed, but we really want fitz
    try:
        import PyPDF2
        PYPDF2_AVAILABLE = True
    except ImportError:
        PYPDF2_AVAILABLE = False

# Word Extraction
import docx

# OpenAI & Embeddings
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Vector DB
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

class DocumentProcessor:
    def __init__(self):
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB is required. Install it with: pip install chromadb")
        
        # Initialize ChromaDB
        try:
            self.client = chromadb.PersistentClient(path="./chroma_db")
        except AttributeError:
             from chromadb.config import Settings
             self.client = chromadb.Client(Settings(
                 chroma_db_impl="duckdb+parquet",
                 persist_directory="./chroma_db"
             ))
             
        self.collection = self.client.get_or_create_collection(name="documents")
        
        # Initialize OpenAI or Fallback
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        
        self.embedding_model = None
        if not self.openai_client:
            try:
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                print("Warning: No local embedding model available.")

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI or local model"""
        # Clean text slightly before embedding to improve quality
        text = text.replace("\n", " ")
        
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"OpenAI embedding error: {e}, using fallback.")
        
        if self.embedding_model:
            return self.embedding_model.encode(text).tolist()
            
        return [0.0] * 384  # Dummy fallback if absolutely nothing works (should not happen)

    def extract_text_from_pdf(self, file_path: Path) -> Tuple[str, List[Tuple[int, str]]]:
        """Extract text using PyMuPDF (fitz) - superior quality"""
        full_text = ""
        pages_data = []
        
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(file_path)
                for page_num, page in enumerate(doc, start=1):
                    # "text" block mode preserves paragraphs better
                    page_text = page.get_text("text") 
                    if page_text.strip():
                        # Clean up headers/footers roughly (simple heuristic)
                        lines = page_text.split('\n')
                        # Remove lonely page numbers
                        lines = [l for l in lines if not (l.strip().isdigit() and len(l.strip()) < 4)]
                        cleaned_page_text = '\n'.join(lines)
                        
                        full_text += cleaned_page_text + "\n\n"
                        pages_data.append((page_num, cleaned_page_text))
                return full_text, pages_data
            except Exception as e:
                print(f"PyMuPDF error: {e}. Falling back to PyPDF2 if available.")
        
        # Fallback
        if PYPDF2_AVAILABLE:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for i, page in enumerate(reader.pages):
                    t = page.extract_text()
                    full_text += t + "\n"
                    pages_data.append((i+1, t))
            return full_text, pages_data
            
        raise ValueError("No PDF extraction library available.")

    def extract_text_from_docx(self, file_path: Path) -> str:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def recursive_chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Smart recursive splitting.
        Priority:
        1. Double newlines (Paragraphs)
        2. Single newlines
        3. Sentences (. )
        4. Words
        """
        if len(text) <= chunk_size:
            return [text]
            
        # 1. Split by paragraphs
        parts = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for part in parts:
            # If adding this part exceeds chunk size, verify if we need to split the PART itself
            if len(current_chunk) + len(part) + 2 > chunk_size:
                # If current_chunk is big enough, push it
                if current_chunk:
                    chunks.append(current_chunk)
                    # Start new chunk with overlap (last N chars)
                    overlap_text = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
                    current_chunk = overlap_text + "\n\n" + part
                else:
                    # The part ITSELF is huge. Split it strictly.
                    current_chunk = part
            else:
                if current_chunk:
                    current_chunk += "\n\n" + part
                else:
                    current_chunk = part
                    
            # If current_chunk became too huge after adding (cases where one huge para exists)
            # FORCE split it using regex (sentences)
            if len(current_chunk) > chunk_size:
                # Naive sentence split
                sentences = re.split(r'(?<=[.!?])\s+', current_chunk)
                
                temp_chunk = ""
                for sent in sentences:
                    if len(temp_chunk) + len(sent) > chunk_size:
                        if temp_chunk:
                            chunks.append(temp_chunk)
                            temp_chunk = sent # No complex overlap here to keep it simple
                        else:
                            # Sentence itself is huge? Just chop it.
                            chunks.append(sent[:chunk_size])
                            temp_chunk = sent[chunk_size:] 
                    else:
                        temp_chunk += " " + sent
                
                current_chunk = temp_chunk # Leftover
                
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def process_document(self, file_path: Path, filename: str) -> str:
        document_id = str(uuid.uuid4())
        
        pages_data = None
        text = ""
        
        if filename.endswith('.pdf'):
            text, pages_data = self.extract_text_from_pdf(file_path)
        elif filename.endswith(('.doc', '.docx')):
            text = self.extract_text_from_docx(file_path)
            pages_data = [(1, text)]
            
        if not text.strip():
            raise ValueError("Empty document")
            
        # Store pages for page-based queries (e.g. "what is on page 5")
        if not hasattr(self, '_document_pages'): self._document_pages = {}
        self._document_pages[document_id] = pages_data
        
        # Smart Chunking
        chunks = self.recursive_chunk_text(text)
        
        # Prepare for DB
        embeddings = []
        ids = []
        metadatas = []
        docs = []
        
        for i, chunk in enumerate(chunks):
            # Try to map chunk back to page number (heuristic)
            page_num = 1
            if pages_data:
                # Simple check: where does this chunk mostly live?
                # We can't be 100% accurate without complex mapping, but let's try matching first 20 chars
                snippet = chunk[:50].strip()
                if snippet:
                    for p_num, p_text in pages_data:
                        if snippet in p_text:
                            page_num = p_num
                            break
            
            emb = self.get_embedding(chunk)
            chunk_id = f"{document_id}_{i}"
            
            embeddings.append(emb)
            ids.append(chunk_id)
            metadatas.append({
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i,
                "page_number": page_num,
                "upload_date": datetime.now().isoformat()
            })
            docs.append(chunk)
            
        self.collection.add(
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
            documents=docs
        )
        
        return document_id

    def search_documents(self, query: str, n_results: int = 5, document_id: str = None) -> List[Tuple[str, float]]:
        """Search and return (text, distance)
        document_id: If provided, only search within this specific document
        """
        try:
            q_emb = self.get_embedding(query)
            
            # Build query with optional document_id filter
            query_params = {
                "query_embeddings": [q_emb],
                "n_results": n_results
            }
            
            # Add document_id filter if provided
            # ChromaDB where filter syntax - try both formats for compatibility
            if document_id:
                try:
                    # Try the $eq operator syntax (newer ChromaDB versions)
                    query_params["where"] = {"document_id": {"$eq": document_id}}
                except:
                    # Fallback to simple equality (older ChromaDB versions)
                    query_params["where"] = {"document_id": document_id}
            
            results = self.collection.query(**query_params)
            
            if not results['documents']:
                return []
                
            docs = results['documents'][0]
            dists = results['distances'][0] if 'distances' in results else [0.0]*len(docs)
            
            return list(zip(docs, dists))
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []

# Singleton
document_processor = DocumentProcessor()
def get_document_processor():
    return document_processor
