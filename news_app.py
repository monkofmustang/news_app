from fastapi import FastAPI
from controller import subscriber_controller, news_controller  # Import routers from controllers
from controller import auth_controller
from db.db_connection import init_indexes

app = FastAPI()

# Register routers
app.include_router(subscriber_controller.router)
app.include_router(news_controller.router)
app.include_router(auth_controller.router)


# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to SROT !"}


@app.on_event("startup")
async def on_startup():
    # Ensure DB indexes exist
    await init_indexes()
