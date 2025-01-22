import aiohttp
from datetime import datetime
from app.db import Database
from app.discord import send_discord_notification

async def check_website(db: Database, site_id : str):
    site = await db.get_site(site_id)
    expected_status = site.get("expected_status_code", 200)
    url = site['url']

    async with aiohttp.ClientSession() as session:
        try:
            start_time = datetime.utcnow()
            async with session.get(url, timeout=10) as response:
                end_time = datetime.utcnow()
                response_time = (end_time - start_time).total_seconds() * 1000
                status = "up" if response.status == expected_status else "down"

        except aiohttp.ClientError:
            status = "down"
            response_time = None

    status_data = {
        "status": status,
        "response_time_ms": response_time,
        "last_checked": datetime.utcnow()
    }   

    if site.get("last_status") == None or status != site.get("last_status"):
        print('Notification will go !!!!!')
        status_data["last_status_change"] = datetime.utcnow()
        await send_discord_notification(site, status_data)

    await db.update_site_status(str(site["_id"]), status_data)

