import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [currentDocumentId, setCurrentDocumentId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Check file type
    const allowedTypes = ['.pdf', '.doc', '.docx'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedTypes.includes(fileExt)) {
      alert('Please upload a PDF, DOC, or DOCX file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/documents/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 120000, // 2 minutes timeout for large files
        }
      );

      // Store the document_id for future queries
      setCurrentDocumentId(response.data.document_id);
      addMessage('assistant', `✅ Document "${response.data.filename}" uploaded and processed successfully! You can now ask questions about it.`);
    } catch (error) {
      console.error('Upload error:', error);
      let errorMessage = 'Unknown error occurred';

      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Upload timeout - file might be too large. Please try a smaller file.';
      } else if (error.response) {
        // Server responded with error
        errorMessage = error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`;
      } else if (error.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to server. Please make sure the backend is running on http://localhost:8000';
      } else {
        errorMessage = error.message || 'Network error';
      }

      addMessage('assistant', `❌ Error uploading document: ${errorMessage}`);
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const addMessage = (role, content) => {
    setMessages((prev) => [...prev, { role, content, timestamp: new Date() }]);
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    addMessage('user', userMessage);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat/`, {
        message: userMessage,
        conversation_id: conversationId,
        document_id: currentDocumentId, // Send current document_id to filter queries
      }, {
        timeout: 60000, // 60 seconds timeout
      });

      addMessage('assistant', response.data.response);

      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }
    } catch (error) {
      console.error('Chat error:', error);
      let errorMessage = 'Unknown error occurred';

      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timeout. The server is taking too long to respond.';
      } else if (error.response) {
        errorMessage = error.response.data?.detail || `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Cannot connect to server. Please make sure the backend is running on http://localhost:8000';
      } else {
        errorMessage = error.message || 'Network error';
      }

      addMessage('assistant', `❌ Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleTextareaChange = (e) => {
    setInputMessage(e.target.value);
    // Auto-resize textarea
    e.target.style.height = 'auto';
    e.target.style.height = e.target.scrollHeight + 'px';
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={() => {
            setMessages([]);
            setConversationId(null);
            setCurrentDocumentId(null);
          }}>
            <span>+</span> New Chat
          </button>
        </div>
        <div className="sidebar-content">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".pdf,.doc,.docx"
            style={{ display: 'none' }}
            id="file-upload"
          />
          <div className="upload-btn-sidebar" onClick={() => fileInputRef.current?.click()}>
            {uploading ? '⏳ Uploading...' : '📄 Upload Document'}
          </div>
        </div>
      </div>

      <div className="main-container">
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-screen">
              <div className="welcome-content">
                <h1>Document Chatbot</h1>
                <p>Upload a document and ask questions about it</p>
                <div className="suggestions">
                  <div className="suggestion-card" onClick={() => fileInputRef.current?.click()}>
                    <span>📄</span>
                    <span>Upload a document</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.role}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 10a3 3 0 100-6 3 3 0 000 6zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" fillRule="evenodd" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="message-bubble">
                <div className="message-text">{msg.content}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-wrapper assistant">
              <div className="message-avatar">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" fillRule="evenodd" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="message-bubble">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-wrapper">
          <div className="input-box">
            <button
              className="attach-button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading || loading}
              title="Upload Document"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
              </svg>
            </button>
            <textarea
              value={inputMessage}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyPress}
              placeholder="Message Document Chatbot..."
              rows="1"
              disabled={loading}
            />
            <button
              className="send-button"
              onClick={sendMessage}
              disabled={loading || !inputMessage.trim()}
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M.5 1.163A1 1 0 011.97.28l12.868 6.837a1 1 0 010 1.766L1.969 15.72A1 1 0 01.5 14.836V10.33a1 1 0 01.816-.983L8.5 8 1.316 6.653A1 1 0 01.5 5.67V1.163z" fill="currentColor" />
              </svg>
            </button>
          </div>
          <p className="input-footer">Document Chatbot can make mistakes. Check important info.</p>
        </div>
      </div>
    </div>
  );
}

export default App;

