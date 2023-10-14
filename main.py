from nicegui import ui
from requests import Session
import time
import os


# Network Session
s = Session()

# Pagination
start = 0
limit = 10


def get_api(url, p=None, s=Session()):
    conn = s.get(url, params=p)
    while not conn.ok:
        print(conn.reason)
        time.sleep(5)
        conn = s.get(url, params=p)
    return conn.json()


def get_opensea_listings(collection, s=Session()):
    listings_url = f"https://api.opensea.io/v2/listings/collection/{collection}/all"
    s.headers.update({
        "accept": "application/json",
        "X-API-KEY": os.getenv('OPENSEA_API_KEY')
    })
    opensea_api = get_api(listings_url, s=s)
    listings = opensea_api['listings']
    while "next" in opensea_api:
        print('next')
        opensea_api = get_api(
            listings_url, {'next': opensea_api['next']}, s)
        listings += opensea_api['listings']

    return sorted(listings, key=lambda l: float(l['price']['current']['value'])/1e18)


def sync():
    global listings
    listings = get_opensea_listings('pixels-farm', s)  # collection slug
    get_farms.refresh()


def next():
    global start
    start += 10
    if start > len(listings) - limit:
        start = len(listings) - limit
    get_farms.refresh()


def prev():
    global start
    start -= 10
    if start < 0:
        start = 0
    get_farms.refresh()


@ui.refreshable
def get_farms() -> None:
    with ui.row():
        ui.button('Previous Page',
                  on_click=prev).enabled = True if start > 0 else False
        ui.button('Next Page', on_click=next).enabled = False if start >= len(
            listings) - limit else True
        ui.button('Sync', on_click=sync)

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


def main():
    sync()
    get_farms()
    ui.run(title='Pixel Farms Opensea',
           dark=True,
           tailwind=False,
           reload=False,
           port=3000
           )


main()
