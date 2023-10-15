from nicegui import app, ui
import opensea


COLLECTION = "pixels-farm"

all_listings = []
# Pagination
start = 0
limit = 10


async def sync():
    global all_listings
    all_listings = await opensea.get_opensea_listings(COLLECTION)
    get_farms.refresh()


def next():
    global start
    start += 10
    if start > len(all_listings) - limit:
        start = len(all_listings) - limit
    get_farms.refresh()


def prev():
    global start
    start -= 10
    if start < 0:
        start = 0
    get_farms.refresh()


@ui.refreshable
def get_farms() -> None:
    global all_listings
    listings = all_listings
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


def main():
    app.on_exception(print)
    app.on_connect(sync())
    get_farms()
    ui.run(title='Pixel Farms Opensea', dark=True, tailwind=False, reload=False, port=3000)

main()
    