from aiohttp import ClientSession

API_URL = f'https://api.openweathermap.org/data/2.5/weather'


async def get_weather(city):
    session = ClientSession()
    params = {'q': city, 'appid': '8ebef75da796ef43be8115869e834322'}
    async with session.get(url=API_URL, params=params) as response:
        weather = await response.json()
    await session.close()
    return f"{city}: {weather['weather'][0]['main']}, temperature: {weather['main']['temp']}"
