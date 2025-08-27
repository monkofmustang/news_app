from fastapi import FastAPI
from controller import subscriber_controller, news_controller  # Import routers from controllers
from controller import ai_controller, international_news_controller, sports_news_controller, tech_news_controller, nepali_news_controller

app = FastAPI()

# Register routers
app.include_router(subscriber_controller.router)
app.include_router(news_controller.router)
app.include_router(ai_controller.router)
app.include_router(international_news_controller.router)
app.include_router(sports_news_controller.router)
app.include_router(tech_news_controller.router)
app.include_router(nepali_news_controller.router)


# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to SROT !"}
