from fastapi import APIRouter, HTTPException
from models.subscribers import Subscribers

# # from db.db_connection import get_collection
#
router = APIRouter(
    prefix="/subscribers",  # All routes will be prefixed with /subscribers
    tags=["Subscribers"],  # Tag for grouping in the documentation
)


# collection = get_collection("subscription")

@router.get("/")
async def codeToSave():
    printf("code not implimented")

# @router.post("/")
# async def create_subscriber(subscriber: Subscribers):
#     # Check if the subscriber already exists
#     existing_subscriber = await collection.find_one({"mobNumber": subscriber.mobNumber})
#     if existing_subscriber:
#         raise HTTPException(status_code=400, detail="Subscriber already exists.")
#
#     # Insert the subscriber into MongoDB
#     result = await collection.insert_one(subscriber.dict())
#     return {"id": str(result.inserted_id), "message": "Subscriber created successfully."}
