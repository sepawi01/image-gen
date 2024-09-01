import os
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_name = "prs-imagegen-images"
blob_container_client = blob_service_client.get_container_client(container_name)


def upload_image_to_blob(image_data, blob_name):
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_client.upload_blob(image_data, overwrite=True)
    return blob_client.url

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

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
