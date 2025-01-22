import aiohttp
from fastapi import HTTPException

async def test_url_connection(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                return 100 <= response.status < 600
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not connect to {url}. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error validating URL {url}: {str(e)}"
        )

