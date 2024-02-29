import os
import sqlite3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app for API operations
app = FastAPI()

# Add CORS middleware to allow requests from the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API key setup
logs_api_key = os.environ['LOGS_API_KEY']
API_KEY_NAME = os.environ['API_KEY_NAME']
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != logs_api_key:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return api_key

class Log(BaseModel):
    response: str
    timestamp: str

def get_db_connection():
    conn = sqlite3.connect('chat_log.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_logs_db():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM chat_logs').fetchall()
    conn.close()
    return [dict(log) for log in logs]

@app.get("/logs/", response_model=List[Log])
async def read_logs():
    logs = fetch_logs_db()
    return logs

@app.post("/log/", response_model=Log, status_code=201)
async def create_log(log: Log, api_key: str = Depends(get_api_key)):
    conn = get_db_connection()
    conn.execute('INSERT INTO chat_logs (response, timestamp) VALUES (?, ?)', (log.response, log.timestamp))
    conn.commit()
    conn.close()
    return log

# start command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
