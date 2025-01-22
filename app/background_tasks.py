from app.db import Database
from app.monitor import check_website
from app.config import settings

async def start_monitoring(app):
    db = Database(app.mongodb)
    sites = await db.get_all_sites()
    
    for site in sites:
        interval = site.get("check_interval_seconds", settings.DEFAULT_CHECK_INTERVAL)
        app.scheduler.add_job(
            check_website,
            'interval',
            seconds=interval,
            args=[db, site['_id']],
            id=f"check_{site['_id']}",
            replace_existing=True
        )

async def add_monitoring_job(app, site):
    db = Database(app.mongodb)
    interval = site.get("check_interval_seconds", settings.DEFAULT_CHECK_INTERVAL)

    # check website status to get it's last status before add it to the scheduler
    await check_website(db, site['_id'])    

    app.scheduler.add_job(
        check_website,
        'interval',
        seconds=interval,
        args=[db, site['_id']],
        id=f"check_{site['_id']}",
        replace_existing=True
    )

async def remove_monitoring_job(app, site_id):
    app.scheduler.remove_job(f"check_{site_id}")

