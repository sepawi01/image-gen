import os
import uuid
from datetime import datetime

from azure.cosmos import CosmosClient

COSMOS_DB_URI = os.getenv("COSMOS_DB_URI")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("COSMOS_DB_DATABASE_NAME")
CONTAINER_NAME = os.getenv("COSMOS_DB_CONTAINER_NAME")

client = CosmosClient(COSMOS_DB_URI, COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def create_image_entry(user_id: str, prompt: str, revised_prompt: str, image_url: str, settings: dict):
    document = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "timestamp": datetime.now(),
        "prompt": prompt,
        "revised_prompt": revised_prompt,
        "image_url": image_url,
        "settings": settings
    }
    container.create_item(body=document)

def get_image_entries_by_user(user_id):
    query = "SELECT * FROM c WHERE c.user=@user ORDER BY c.timestamp DESC"
    parameters = [{"name": "@user", "value": user_id}]
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        partition_key=user_id
    ))
    return items