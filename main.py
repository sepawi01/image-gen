import base64
import hashlib
import urllib
from contextlib import asynccontextmanager
from typing import Literal, AsyncGenerator
import os

from markdown_it.rules_inline import image
from openai import AzureOpenAI, BadRequestError

import json
from PIL import Image
import httpx
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv

from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings

from fastapi import FastAPI, Request, Security, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from fastapi_azure_auth.user import User
load_dotenv()


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = ['http://localhost:8000']
    AZURE_OPENAI_API_KEY: str = ""
    OPENAPI_CLIENT_ID: str = ""
    APP_CLIENT_ID: str = ""
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()
    yield


def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')

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

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    tenant_id=settings.TENANT_ID,
    scopes=settings.SCOPES,
)

OPENAI_CLIENT = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://prs-open-ai-service.openai.azure.com/",
    api_key=settings.AZURE_OPENAI_API_KEY,
)



@app.get("/", operation_id="get_root")
async def root(user: User = Depends(azure_scheme)):
    return FileResponse("static/index.html")

@app.get(
    '/hello-user',
    response_model=User,
    operation_id='helloWorldApiKey',
    dependencies=[Depends(azure_scheme)]
)
async def hello_user(request: Request) -> dict[str, bool]:
    """
    Wonder how this auth is done?
    """
    return request.state.user.dict()
@app.get("/api/generate", dependencies=[Security(azure_scheme)])
async def generate(prompt: str,
                   n: int = 1,
                   quality: Literal["standard", "hd"] = "standard",
                   size: Literal['1024x1024', '1792x1024', '1024x1792'] = "1024x1024",
                   style: Literal["vivid", "natural"] = "natural"
                   ,user: User = Depends(azure_scheme)
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

session = {}
@app.get("/auth-redirect")
async def auth_redirect(code: str):
    code_verifier = session.get('code_verifier')

    data = {
        "grant_type": "authorization_code",
        "client_id": settings.APP_CLIENT_ID,
        "code": code,
        "redirect_uri": settings.AUTH_REDIRECT_URI,
        "code_verifier": code_verifier,
        "scope": settings.SCOPE_NAME,
    }

    response = httpx.post(settings.OPENAPI_TOKEN_URL, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data
    else:
        return {"error": "Failed to exchange code for token"}



@app.get("/login")
def login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    auth_url = (
        f"{settings.OPENAPI_AUTHORIZATION_URL}"
        f"?client_id={settings.APP_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={urllib.parse.quote(settings.AUTH_REDIRECT_URI)}"
        f"&response_mode=query"
        f"&scope={urllib.parse.quote(settings.SCOPE_NAME)}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    session['code_verifier'] = code_verifier
    return RedirectResponse(url=auth_url)
#
#
# @app.get("/auth-required")
# async def auth_required(user: User = Security(azure_scheme)):
#     if user is None:
#         return RedirectResponse(url=azure_scheme.create_authorization_url())
#     return JSONResponse(content={"message": "User is authenticated"}, status_code=200)
#
# @app.exception_handler(HTTPException)
# async def auth_exception_handler(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#         return RedirectResponse(url=azure_scheme.create_authorization_url())
#     return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)