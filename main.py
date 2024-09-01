from typing import Literal, AsyncGenerator
import os
from openai import AzureOpenAI, BadRequestError
import json
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings
from fastapi import FastAPI, Request, Security, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = ['http://localhost:8000']
    AZURE_OPENAI_API_KEY: str = ""
    OPENAPI_CLIENT_ID: str = ""
    APP_CLIENT_ID: str = ""
    APP_CLIENT_SECRET: str = ""
    AUTH_REDIRECT_URI: str = ""
    TENANT_ID: str = os.getenv("TENANT_ID")
    SCOPE_DESCRIPTION: str = "user_impersonation"

    @computed_field
    @property
    def SCOPE_NAME(self) -> str:
        return f'api://{self.APP_CLIENT_ID}/{self.SCOPE_DESCRIPTION}'

    @computed_field
    @property
    def SCOPES(self) -> dict:
        return {
            self.SCOPE_NAME: self.SCOPE_DESCRIPTION,
        }

    @computed_field
    @property
    def OPENAPI_AUTHORIZATION_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/authorize"

    @computed_field
    @property
    def OPENAPI_TOKEN_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/token"

        class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'
            case_sensitive = True


settings = Settings()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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

OPENAI_CLIENT = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://prs-open-ai-service.openai.azure.com/",
    api_key=settings.AZURE_OPENAI_API_KEY,
)


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/api/generate")
async def generate(prompt: str,
                   n: int = 1,
                   quality: Literal["standard", "hd"] = "standard",
                   size: Literal['1024x1024', '1792x1024', '1024x1792'] = "1024x1024",
                   style: Literal["vivid", "natural"] = "natural"
                   ):
    try:
        result = OPENAI_CLIENT.images.generate(
            model="PRS-Dall-e-3",
            prompt=prompt,
            n=n,
            quality=quality,
            size=size,
            style=style
        )

        data = json.loads(result.model_dump_json())['data']
        return JSONResponse(content=data)
    except BadRequestError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True)
