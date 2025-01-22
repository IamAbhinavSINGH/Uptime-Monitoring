from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

class Database:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def add_site(self, site_data: dict) -> str:
        site_data["created_at"] = datetime.utcnow()
        result = await self.db.sites.insert_one(site_data)
        return str(result.inserted_id)

    async def remove_site(self, site_id: str) -> bool:
        result = await self.db.sites.delete_one({"_id": ObjectId(site_id)})
        return result.deleted_count > 0

    async def get_site(self , site_id : str) -> dict: 
        site = await self.db.sites.find_one({"_id": ObjectId(site_id)})
        if site:
            # Convert ObjectId to string
            site["_id"] = str(site["_id"])
        return site

    async def get_all_sites(self):
        cursor = self.db.sites.find()
        sites = await cursor.to_list(length=None)
        return [{**site, "_id": str(site["_id"])} for site in sites]

    async def get_site_history(self, site_id: str):
        cursor = self.db.status_checks.find({"site_id": ObjectId(site_id)}).sort("last_checked", -1)
        history = await cursor.to_list(length=None)
        return [{**check, "_id": str(check["_id"]), "site_id": str(check["site_id"])} for check in history]

    async def update_site_status(self, site_id: str, status_data: dict):
        status_data["site_id"] = ObjectId(site_id)
        status_data["created_at"] = datetime.utcnow()
        await self.db.status_checks.insert_one(status_data)
        await self.db.sites.update_one(
            {"_id": ObjectId(site_id)},
            {"$set": {
                "last_status": status_data["status"],
                "last_checked": status_data["last_checked"],
                "last_status_change": status_data.get("last_status_change")
            }}
        )

    async def add_webhook_url(self , site_id : str , webhook_url : str):
        await self.db.sites.update_one(
            {"_id" : ObjectId(site_id)},
            {"$set" : {
                "webhook_url" : webhook_url
            }}
        )
