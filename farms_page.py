from nicegui import ui
from opensea import get_opensea_listings

COLLECTION = "pixels-farm"

@ui.page('/farms', response_timeout=999)
async def farms():
    
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row():
            ui.button('Farms', on_click=lambda: ui.open('/farms'))
            ui.button('Pets', on_click=lambda: ui.open('/pets'))

    listings = []
    # Pagination
    start = 0
    limit = 10

    def next():
        nonlocal start
        start += 10
        if start > len(listings) - limit:
            start = len(listings) - limit
        get_farms.refresh()


    def prev():
        nonlocal start
        start -= 10
        if start < 0:
            start = 0
        get_farms.refresh()
        

    async def sync():
        nonlocal listings
        listings = await get_opensea_listings(COLLECTION)
        get_farms.refresh()

    @ui.refreshable
    def get_farms() -> None:
        nonlocal listings
        with ui.row():
            ui.button('Previous Page',
                    on_click=prev).enabled = True if start > 0 else False
            ui.button('Next Page', on_click=next).enabled = False if start >= len(
                listings) - limit else True
            ui.button('Sync', on_click=sync)
        if listings:
            with ui.row().style('justify-content: space-evenly'):

                for i in range(start, start + limit):
                    id = listings[i]['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
                    price = float(listings[i]['price']['current']['value'])/1e18
                    with ui.card().tight().style('width: 18.5vw').classes('no-shadow border-[0px]'):
                        ui.html(
                            f"<iframe width=100% height='270vh' src='https://play.pixels.xyz/pixels/share/{id}'></iframe>")
                        with ui.card_section():
                            ui.label(f'Farm Land #{id}')
                            ui.label(f'Price: {price:.4f} ETH')
        else:
            ui.label("No listings found")
    
    get_farms()
    await sync()