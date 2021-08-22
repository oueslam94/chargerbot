import asyncio
import pyjuicenet
import aiohttp
import os

async def get_chargers():
  async with aiohttp.ClientSession() as session:
    api = pyjuicenet.Api(os.environ['JUICENET_API_KEY'], session)
    devices = await api.get_devices()
    return devices