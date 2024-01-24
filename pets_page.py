from nicegui import ui
from async_api import HunterAPI
from dotenv import load_dotenv
from datetime import datetime
import os, asyncio

load_dotenv()
MAVIS_API_KEY = os.getenv("MAVIS_API_KEY")
TOKEN_ADDRESS = "0xb806028b6ebc35926442770a8a8a7aeab6e2ce5c"
GRAPHQL_ENDPOINT = "https://api-gateway.skymavis.com/graphql/mavis-marketplace"

mavis_api = HunterAPI()
mavis_api.set_api_key(MAVIS_API_KEY)

@ui.page('/pets', response_timeout=999)
async def pets():

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row():
            ui.button('Farms', on_click=lambda: ui.open('/farms'))
            ui.button('Pets', on_click=lambda: ui.open('/pets'))
    
    start = 0
    limit = 10
    sales = []
    ronin_price = 0

    async def get_sales_history():
        nonlocal start, sales

        body = f'''query GetSalesHistory {{
            recentlySolds(
                from: {start}
                size: {limit+1}
                tokenAddress: "{TOKEN_ADDRESS}"
            ) {{
                results {{
                realPrice
                assets {{
                    id
                }}
                timestamp
                }}
            }}
            }}
        '''

        async def get_token(id):
            body = f'''query GetToken {{
                erc721Token(
                    tokenAddress: "0xb806028b6ebc35926442770a8a8a7aeab6e2ce5c"
                    tokenId: "{id}"
                ) {{
                    image
                    name
                }}
                }}
            '''
            response = await mavis_api.get(GRAPHQL_ENDPOINT, {'query': body})
            return response.json()['data']['erc721Token']
        

        response = await mavis_api.get(GRAPHQL_ENDPOINT, {'query': body})
        sales = response.json()['data']['recentlySolds']['results']
        
        tasks = [ asyncio.create_task(get_token(item['assets'][0]['id'])) for item in sales[:limit] ]
        tokens = await asyncio.gather(*tasks)

        for id in range(len(sales)-1):
            sales[id]['image'] = tokens[id]['image']
            sales[id]['name'] = tokens[id]['name']

    async def next():
        nonlocal start, sales
        start += 10
        if len(sales) == 0:
            start -= 10
        else:
            await get_sales_history()
            sales_history.refresh()

    async def prev():
        nonlocal start
        start -= 10
        if start < 0:
            start = 0
        await get_sales_history()
        sales_history.refresh()

    async def get_usd_price(token):
        response = await mavis_api.get('https://api.coingecko.com/api/v3/simple/price',
                                       {'ids': token, 'vs_currencies': 'usd'})
        prices = response.json()
        return prices[token]['usd']

    @ui.refreshable
    def sales_history() -> None:
        nonlocal sales, ronin_price

        with ui.row():
            ui.button('Previous Page',
                      on_click=prev).enabled = True if start > 0 else False
            ui.button('Next Page', on_click=next).enabled = True if len(
                sales) > limit else False

        if sales:
            with ui.row().style('justify-content: space-evenly'):

                for item in sales[:limit]:
                    ron = float(item['realPrice'])/1e18
                    with ui.card().tight().style('width: 18.5vw'):
                        ui.image(item['image'])
                        with ui.card_section():
                            ui.label(
                                f"Name: {item['name']}")
                            ui.label(
                                f"PET #{item['assets'][0]['id']}")
                            ui.label(
                                f"Sold @ {ron} RON (${(ron*ronin_price):,.2f})")
                            ui.label(datetime.fromtimestamp(
                                item['timestamp']).strftime('%d %B %Y %I:%M %p'))
        else:
            ui.label("No listings found")

    await get_sales_history()
    ronin_price = await get_usd_price('ronin')
    sales_history()
