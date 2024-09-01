#%%
# Add test data to the database
from backend.services import cosmosdb_service

test_data = {"user_id": "123",
    "prompt": "Just some random prompt. This is test data",
    "revised_prompt": "This is the revised prompt",
    "image_url": "https://dalleprodsec.blob.core.windows.net/private/images/5c29ae81-439a-4c62-aeb4-6ac2f7d0f203/generated_00.png?se=2024-09-01T14%3A22%3A48Z&sig=g6X%2BriXkdsFMbO8ThZTK0MzvHPAjKIEwHgc67Agmtvw%3D&ske=2024-09-06T11%3A50%3A27Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-08-30T11%3A50%3A27Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02",
    "settings": {
        "quality": "standard",
        "size": "1024x1024",
        "style": "natural"
}
}
cosmosdb_service.create_image_entry(**test_data)

#%%
# Get data from the database
from backend.services import cosmosdb_service
data = cosmosdb_service.get_image_entries_by_user("123")





