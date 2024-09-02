import json
import uuid
from typing import Literal

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from openai import BadRequestError, AzureOpenAI
from backend.settings import settings
from backend.services import cosmosdb_service, blobstorage_service

router = APIRouter(
    prefix="/api",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

OPENAI_CLIENT = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://prs-open-ai-service.openai.azure.com/",
    api_key=settings.AZURE_OPENAI_API_KEY,
)


@router.get("/images/user/{user_id}")
async def get_images(user_id: str):
    user_images = cosmosdb_service.get_image_entries_by_user(user_id)
    # Add SAS token to each image URL
    for image in user_images:
        image["imageUrl"] = blobstorage_service.generate_sas_url(image["blobName"])

    return JSONResponse(content=user_images)

@router.get("/images/blob/{blob_name}")
async def get_image_url(blob_name:str):
    # Add SAS token to each image URL
    image_url = blobstorage_service.generate_sas_url(blob_name)
    return JSONResponse(content={"imageUrl": image_url})

@router.post("/images/generate")
async def generate_images(user_id: str,
                          prompt: str,
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

        data = json.loads(result.model_dump_json())["data"]

        # Save the generated images to Azure Blob Storage
        new_image_urls, blob_names = await blobstorage_service.process_images(user_id, data)

        images_data = []
        # Upload to CosmosDB
        for i, image_data in enumerate(data):
            image_settings = {
                "quality": quality,
                "size": size,
                "style": style
            }
            cosmosdb_service.create_image_entry(user_id,
                                                prompt,
                                                image_data["revised_prompt"],
                                                new_image_urls[i],
                                                blob_names[i],
                                                image_settings
                                                )
            images_data.append({
                "prompt": prompt,
                "revised_prompt": image_data["revised_prompt"],
                "imageUrl": new_image_urls[i],
                "blobName": blob_names[i],
                "imageSettings": image_settings
            })

        return JSONResponse(content=images_data)
    except BadRequestError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
