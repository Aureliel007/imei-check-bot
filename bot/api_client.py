import aiohttp
import asyncio

from config import load_config


imei_api_token = load_config().imei_api_token

async def get_imei_info(imei: str):
    url = 'https://api.imeicheck.net/v1/checks'
    headers = {'Authorization': f'Bearer {imei_api_token}'}
    params = {"deviceId": imei, "serviceId": 13}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=params) as response:
            data = await response.json()
            return data
        