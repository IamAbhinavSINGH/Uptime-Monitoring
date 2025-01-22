from fastapi import APIRouter, Request, HTTPException
from bson import ObjectId
from app.db import Database
from app.models import Website, WebsiteResponse
from app.utils import test_url_connection
from app.background_tasks import add_monitoring_job, remove_monitoring_job

router = APIRouter()

@router.post("/sites", response_model=WebsiteResponse)
async def add_site(request: Request, site: Website):
    # First validate the URL by making a test connection
    await test_url_connection(str(site.url))
    
    # Convert Pydantic model to dict
    site_dict = site.model_dump()
    
    # Convert HttpUrl to string
    site_dict["url"] = str(site_dict["url"])
    
    # Add to database
    db = Database(request.app.mongodb)
    site_id = await db.add_site(site_dict)
    
    # Add the ID to the dict for monitoring
    site_dict["_id"] = site_id
    
    # Start monitoring
    await add_monitoring_job(request.app, site_dict)
    
    return {
        "id": site_id,
        **site_dict
    }


@router.delete("/sites/{site_id}")
async def remove_site(request: Request, site_id: str):
    db = Database(request.app.mongodb)
    if await db.remove_site(site_id):
        await remove_monitoring_job(request.app, site_id)
        return {"message": "Site removed successfully"}
    raise HTTPException(status_code=404, detail="Site not found")


@router.get("/sites")
async def list_sites(request: Request):
    db = Database(request.app.mongodb)
    sites = await db.get_all_sites()
    return sites


@router.get("/sites/{site_id}/history")
async def get_site_history(request: Request, site_id: str):
    db = Database(request.app.mongodb)
    history = await db.get_site_history(site_id)
    return history


@router.post("/webhook")
async def set_discord_webhook(request: Request, webhook_data: dict):
    if(webhook_data.get("url") == None):
        return { "message" : "webhook url can't be empty" }
    
    db = Database(request.app.mongodb)
    request.app.state.settings.DISCORD_WEBHOOK_URL = webhook_data["url"]
    
    returnMsg = {
        "message" : "Webhook URL updated successfully"
    }

    print(webhook_data.get("website_id"))
    if(webhook_data.get("website_id") != None):
        if(await db.get_site(webhook_data['website_id'])):
            await db.add_webhook_url(webhook_data["website_id"] , webhook_url=webhook_data['url'])
    else:
        returnMsg["info"] = "consider adding 'website_id' to send notifications of particular website to different channels"
    
    return returnMsg

