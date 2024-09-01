import os
import uuid
from io import BytesIO

import httpx
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_name = "prs-imagegen-images"
blob_container_client = blob_service_client.get_container_client(container_name)


def upload_image_to_blob(image_data, blob_name):
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_client.upload_blob(image_data, overwrite=True)
    return blob_client.url


async def process_images(user_id, data):
    image_urls = []
    image_blob_names = []
    for image_data in data:
        blob_name = f"{user_id}/{str(uuid.uuid4())}.png"

        # Download the image from the URL
        async with httpx.AsyncClient() as client:
            response = await client.get(image_data["url"])
            response.raise_for_status()  # Ensure we got a valid response

        # Use a BytesIO buffer to hold the image data
        image_buffer = BytesIO(response.content)

        # Upload the image to blob storage
        image_url = upload_image_to_blob(image_buffer, blob_name)
        image_urls.append(image_url)
        image_blob_names.append(blob_name)

    return image_urls, image_blob_names


def generate_sas_url(blob_name):
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day
    )
    blob_url_with_sas = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return blob_url_with_sas
