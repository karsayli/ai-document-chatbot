import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Any
from app.services.document_processor import get_document_processor

class RAGService:
    def __init__(self):
        self._processor = None
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if self.google_api_key:
            try:
                genai.configure(api_key=self.google_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                print("DEBUG: Gemini 2.0 Flash Connected")
            except Exception as e:
                print(f"Gemini Init Error: {e}")
                self.gemini_model = None
        else:
            self.gemini_model = None
    
    @property
    def document_processor(self):
        if self._processor is None:
            self._processor = get_document_processor()
        return self._processor

    def generate_response(self, query: str, context_chunks: List[str], history: List[Dict[str, str]] = []) -> str:
        """
        Generate response using History + Document Context
        """
        context_str = "\n\n---\n\n".join(context_chunks) if context_chunks else "No relevant document section found."
        
        # Build Chat History String for Prompt
        chat_history_str = ""
        # Take last 5 messages to avoid token limit, skipping the very last one (which is the current query)
        recent_history = history[-6:-1] if len(history) > 1 else [] 
        
        for msg in recent_history:
            role = "User" if msg['role'] == 'user' else "AI"
            chat_history_str += f"{role}: {msg['content']}\n"

        system_instruction = """You are a Document Analysis AI. Your primary mission is to answer questions based on the provided document.

[STRICT RULES]
1. **PRIORITY**: You MUST look for the answer in the [Document Content] first. Search thoroughly through all provided document chunks.
2. **SOURCE TRUTH**: For specific fact-checking, use ONLY the document. Extract information directly from the document content.
3. **CREATIVE TASKS**: If the user asks for summaries, quizzes, or lists (e.g. "10 questions"), you may EXTRAPOLATE from the provided content to generate full results, as long as they are relevant to the document topics. However, when answering those questions, you MUST base your answers on the document content provided.
4. **LANGUAGE**: You MUST ALWAYS respond in ENGLISH, regardless of the language of the user's question. If the document is in a different language, translate the relevant information to English. Never respond in Turkish or any other language - always use English.
5. **FALLBACK**: Only if the document is completely silent on the topic after thorough searching, you may use your general knowledge, but you MUST clearly state "This information is not found in the uploaded document. Based on general knowledge: [answer]"
6. **IMPORTANT**: When the user asks "what does the PDF say?" or "what about is pdf", they are asking about the CONTENT of the uploaded document, NOT about PDFs as a file format. Always answer based on the document content provided.
7. **ANSWER ACCURACY**: When answering questions about the document, quote or reference specific information from the document. If you cannot find the answer in the provided document chunks, state clearly: "I could not find a direct answer to this question in the uploaded document." Do not make up answers."""

        user_prompt = f"""[Conversation History]
{chat_history_str}

[Document Content]
{context_str}

[Current User Question]
{query}

**IMPORTANT INSTRUCTIONS:**
- You MUST answer based on the [Document Content] provided above
- Search through all the document chunks carefully to find relevant information
- If the question asks you to answer questions from a list, use the document content to answer each one
- Quote specific information from the document when possible
- If information is not in the document, clearly state that
- Always respond in ENGLISH only

Answer:"""

        # 1. Gemini
        if self.gemini_model:
            try:
                # Use proper Gemini API format - combine system instruction and user prompt
                full_prompt = f"{system_instruction}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                    )
                )
                return response.text
            except Exception as e:
                print(f"Gemini Error: {e}")
                # Try without generation_config if it fails
                try:
                    full_prompt = f"{system_instruction}\n\n{user_prompt}"
                    response = self.gemini_model.generate_content(full_prompt)
                    return response.text
                except Exception as e2:
                    print(f"Gemini Error (retry): {e2}")
                    return f"⚠️ Error generating response: {str(e2)}"
        
        # 2. OpenAI Fallback
        processor = self.document_processor
        if processor.openai_client:
            try:
                full_prompt = f"{system_instruction}\n\n{user_prompt}"
                response = processor.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI Error: {e}")

        # 3. No Brain Fallback
        if not context_chunks:
            return "I am in Offline Mode (No AI Key). I can only search specific terms, not chat."
            
        return "Offline Mode - Search Results:\n" + "\n".join(context_chunks[:2])

    def query(self, user_query: str, history: List[Dict[str, str]] = [], document_id: str = None) -> Tuple[str, List[str]]:
        """
        Stateful Query Handler
        document_id: If provided, only search within this specific document
        """
        processor = self.document_processor
        
        # Preprocess query: Remove generic terms that don't help search
        # If user asks "what does the PDF say?", search for document content instead
        search_query = user_query.lower()
        
        # Replace generic PDF/document queries with better search terms
        if any(phrase in search_query for phrase in ["what does the pdf say", "what about is pdf", "what is in the pdf", "pdf say", "document say"]):
            # Try to get any content from documents - use a very generic query
            search_query = "content information text"
        else:
            # Use original query but remove stop words that might interfere
            # Keep the original query for semantic search
            search_query = user_query
        
        # 2. Search Vector DB
        # Dynamic Context Limit: Increase window for broad generation tasks and question answering
        broad_keywords = ['summary', 'summarize', 'overview', 'questions', 'quiz', 'list', 'create', 'generate', 'answer']
        question_keywords = ['what', 'how', 'why', 'when', 'where', 'who', 'explain', 'describe', 'tell']
        
        # Increase limit for better context retrieval
        if any(k in user_query.lower() for k in broad_keywords):
            limit = 15
        elif any(k in user_query.lower() for k in question_keywords):
            limit = 12
        else:
            limit = 8
        
        results = processor.search_documents(search_query, n_results=limit, document_id=document_id)
        
        context_chunks = []
        if results:
            # Filter out results with very high distance (low similarity)
            # Keep results with distance < 1.5 (lower is better for cosine distance)
            context_chunks = [doc for doc, dist in results if dist < 1.5]
            # If we filtered too much, include some more
            if len(context_chunks) < 3 and results:
                context_chunks = [doc for doc, dist in results[:limit]]
        
        # If no results found, try a more generic search
        if not context_chunks:
            # Try searching with just common words from the query
            words = [w for w in user_query.lower().split() if len(w) > 3 and w not in ['what', 'does', 'the', 'pdf', 'say', 'about', 'is', 'are', 'can', 'you', 'this', 'that', 'these', 'those']]
            if words:
                fallback_query = " ".join(words[:5])  # Use first 5 meaningful words
                fallback_results = processor.search_documents(fallback_query, n_results=8, document_id=document_id)
                if fallback_results:
                    context_chunks = [doc for doc, dist in fallback_results if dist < 1.5]
                    if not context_chunks and fallback_results:
                        context_chunks = [doc for doc, dist in fallback_results[:5]]
            
        # If still no results, try to get ANY document content (more chunks for better context)
        if not context_chunks:
            try:
                # Get documents from collection, filtered by document_id if provided
                if document_id:
                    # Get only chunks from the specified document
                    try:
                        # Try the $eq operator syntax (newer ChromaDB versions)
                        all_results = processor.collection.get(
                            where={"document_id": {"$eq": document_id}}
                        )
                    except:
                        # Fallback to simple equality (older ChromaDB versions)
                        all_results = processor.collection.get(
                            where={"document_id": document_id}
                        )
                else:
                    # Get all documents
                    all_results = processor.collection.get()
                    
                if all_results and all_results.get('documents'):
                    # Get more chunks as context to improve answer quality
                    context_chunks = all_results['documents'][:10]
            except Exception as e:
                print(f"Fallback search error: {e}")
            
        # 3. Generate Logic
        response = self.generate_response(user_query, context_chunks, history)
        
        sources = ["Document"] if context_chunks else ["General Knowledge"]
        return response, sources

rag_service = RAGService()
