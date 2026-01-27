#!/bin/bash
echo "Starting Document Chatbot Backend..."
python -m uvicorn app.main:app --reload --port 8000

