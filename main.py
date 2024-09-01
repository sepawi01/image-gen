from typing import Literal, AsyncGenerator
import os
from fastapi import FastAPI, Request, Security, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.settings import settings

from backend.routes import images


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(images.router)

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("static/index.html")





if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True, log_level="debug")
