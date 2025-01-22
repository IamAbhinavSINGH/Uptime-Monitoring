import aiohttp
from app.config import settings

async def send_discord_notification(site: dict, status_data: dict):
    webhook_url = site.get("webhook_url") or settings.DISCORD_WEBHOOK_URL
    if not webhook_url:
        print("No webhook url set to send notifcations!!!")
        return

    status = status_data["status"]
    emoji = "🟢" if status == "up" else "🔴"
    title = f"{emoji} Website {'Recovery' if status == 'up' else 'Down'} Alert"

    message = f"""
    Site: {site.get('name', site['url'])} ({site['url']})
    Status: {'UP' if status == 'up' else 'DOWN'}
    Time: {status_data['last_checked'].strftime('%Y-%m-%d %H:%M:%S')} UTC
    """

    if status == "down":
        message += f"Error: Unable to connect or unexpected status code"
    elif status == "up" and "last_status_change" in status_data:
        downtime = status_data['last_checked'] - status_data['last_status_change']
        message += f"Downtime Duration: {downtime}"

    payload = {
        "content": title,
        "embeds": [{
            "description": message,
            "color": 65280 if status == "up" else 16711680
        }]
    }

    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)

