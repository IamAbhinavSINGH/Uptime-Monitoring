from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routes import router
from app.config import settings
from app.background_tasks import start_monitoring

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]
    
    # Initialize the scheduler
    app.scheduler = AsyncIOScheduler()
    app.scheduler.start()
    
    # Start the monitoring tasks
    await start_monitoring(app)

    # Add settings to the app
    app.state.settings = settings

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    app.scheduler.shutdown()

app.include_router(router, prefix="/api")

