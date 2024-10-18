from fastapi import FastAPI
from controller import subscriber_controller, news_controller  # Import routers from controllers

app = FastAPI()

# Register routers
app.include_router(subscriber_controller.router)
app.include_router(news_controller.router)


# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Nepal News!"}
