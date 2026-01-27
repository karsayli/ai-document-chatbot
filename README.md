# Document Chatbot

A complete RAG (Retrieval-Augmented Generation) system with a chatbot interface. Users can upload documents (PDF, DOC, DOCX) and interact with them through a conversational interface powered by Google Gemini 2.0 Flash.

**Created by: Aylin Kars**

## Quick Start

1. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Create .env file with GOOGLE_API_KEY
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000

**Windows Users:** Use `START_BACKEND.bat` and `START_FRONTEND.bat` for easier startup.

## Features

- 📄 **Document Upload**: Support for PDF, DOC, and DOCX files
- 🔍 **Vector Search**: ChromaDB for efficient semantic search
- 🤖 **Smart Chatbot**: Ask questions and get answers based on your documents
- ⚡ **FastAPI Backend**: High-performance async API
- ⚛️ **React Frontend**: Modern, responsive UI
- 📄 **Page-specific Queries**: Ask about specific pages (e.g., "what is on page 5")
- 💬 **ChatGPT-like Interface**: Natural conversation support
- 🧠 **Gemini 2.0 Flash**: Powered by Google's Gemini AI for intelligent responses
- 🔄 **Smart Query Processing**: Automatic query preprocessing for better document retrieval
- 📚 **Multi-document Support**: Process and query multiple documents
- 🌐 **English-only Responses**: All responses are in English for consistency
- 🎯 **Document Filtering**: Each conversation is tied to a specific document

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API keys (create a `.env` file in the `backend/` directory):
```bash
# Create .env file in backend/ directory
GOOGLE_API_KEY=your-google-api-key-here
OPENAI_API_KEY=your-openai-api-key-here  # Optional, for embeddings
```

**API Keys:**
- **GOOGLE_API_KEY** (Required): Required for Gemini 2.0 Flash chat responses. Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OPENAI_API_KEY** (Optional): For better embeddings. If not set, sentence-transformers will be used as fallback.

**Note**: The system requires at least one API key. Google API key is recommended for chat functionality.

5. Run the backend server:

**Windows:**
```bash
# Option 1: Use the batch file
START_BACKEND.bat

# Option 2: Manual start
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Mac/Linux:**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

**Quick Start:**
- Health check: `http://127.0.0.1:8000/api/health`
- API status: `http://127.0.0.1:8000/`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:

**Windows:**
```bash
# Option 1: Use the batch file
START_FRONTEND.bat

# Option 2: Manual start
npm start
```

**Mac/Linux:**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start Backend**: Run the backend server (see Setup Instructions above)
2. **Start Frontend**: Run the frontend server in a separate terminal
3. **Upload a Document**: Click the "Upload Document" button and select a PDF, DOC, or DOCX file
4. **Wait for Processing**: The document will be processed and indexed (this may take a moment)
5. **Start Chatting**: Type questions about your document in the chat interface
6. **Get Answers**: The system will retrieve relevant information from your document and generate intelligent responses using Gemini AI

### Example Queries

- "What does the PDF say?"
- "Summarize the document"
- "What is on page 5?"
- "Create 10 questions about this document"
- "What are the main topics?"

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload and process a document
- `GET /api/documents/list` - List processed documents

### Chat
- `POST /api/chat/` - Send a chat message
- `GET /api/chat/conversation/{conversation_id}` - Get conversation history

## Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **ChromaDB**: Vector database for embeddings
- **PyMuPDF (fitz)**: High-quality PDF text extraction
- **python-docx**: DOCX text extraction
- **Google Gemini 2.0 Flash**: AI chat generation (primary)
- **OpenAI API** (optional): For embeddings and chat generation fallback
- **sentence-transformers** (fallback): Local embeddings model

### Frontend
- **React**: UI library
- **Axios**: HTTP client
- **CSS3**: Modern styling

## Notes

- Documents are processed and stored in a local ChromaDB instance (`backend/chroma_db/`)
- Conversations are stored in memory (not persisted across server restarts)
- Uploaded files are temporarily stored in `backend/uploads/` directory
- The system uses smart query preprocessing to better understand user questions
- All responses are in English only
- Each conversation is tied to a specific document for accurate answers

## Troubleshooting

### Backend Issues
- Ensure all Python dependencies are installed
- Check that port 8000 is not in use
- Verify file permissions for uploads directory

### Frontend Issues
- Ensure Node.js and npm are installed
- Try clearing npm cache: `npm cache clean --force`
- Check that port 3000 is not in use

### Embedding Issues
- If OpenAI API is not available, sentence-transformers will be used automatically
- First run may take longer as models are downloaded
- Ensure `.env` file exists in `backend/` directory with `GOOGLE_API_KEY`

### Chat Issues
- Make sure Gemini API key is set in `.env` file
- Check backend logs for detailed error messages
- All responses will be in English regardless of question language

## License

MIT License - Created by Aylin Kars
