from dotenv import load_dotenv
from async_api import HunterAPI
import os, asyncio

load_dotenv()
# Opensea API Key
OPENSEA_API_KEY = os.getenv("OPENSEA_API_KEY")
HunterAPI.client.headers = {"X-API-KEY": OPENSEA_API_KEY}


async def refresh_metadata(network: str, address: str, token: str | int, sleep: int = 0):
    """Requests an NFT metadata update to opensea.

    Parameters
    ----------
    network : string
        Blockchain network ex.(ethereum, matic).
    address : string
        Contract Address of the NFT collection.
    token : string or int
        Token number of the NFT.
    sleep : int (optional)
        Adds a wait time after the request for the metadata to update.
    """

    url = f"https://api.opensea.io/v2/chain/{network}/contract/{address}/nfts/{token}/refresh"
    await HunterAPI.post(url)
    await asyncio.sleep(sleep)


async def get_collection_info(collection: str) -> dict:
    """Gets the contract address, metadata url, and a token number of an opensea collection.

    Parameters
    ----------
    collection : string
        Opensea collection slug.

    Returns
    -------
    dictionary
        The contract address, metadata url, and a sample token number of the opensea collection.
        Keys: contract_address, metadata_url, token
    """

    url = f"https://api.opensea.io/v2/collection/{collection}/nfts"
    response = await HunterAPI.get(url, {'limit': '1'})
    nft = response.json()['nfts'][0]

    contract_address = nft['contract']
    metadata_url = nft['metadata_url']
    token = metadata_url.split('/')[-1]
    metadata_url = nft['metadata_url'].replace(token, "")

    return {'contract_address' : contract_address, 'metadata_url' : metadata_url, 'token': token}


async def get_owners(contract: str, token: str, network: str) -> dict:
    """Gets the owner count and addresses of an ERC-1155 NFT.

    Parameters
    ----------
    contract : string
        Contract address of the NFT Collection.
    token: string
        Token number of the ERC-1155 NFT
    network: string
        The blockchain that the NFT uses. ex.(ethereum, matic)

    Returns
    -------
    dictionary
        The nft details, owners and how many NFT each owners owns.\n
        { identifier: "", collection: "", contract: "", token_standard: "", name: "", description: "",
        image_url: "", metadata_url: "", created_at: "", updated_at: "", is_disabled: bool, is_nsfw: bool,
        animation_url: "", is_suspicious: bool, creator: "" | null, traits: "" | null, rarity: "" | null\n
        owners: [ { address: "", quantity: "" } ] }
    """
    url = f"https://api.opensea.io/api/v2/chain/{network}/contract/{contract}/nfts/{token}"
    response = await HunterAPI.get(url)
    
    return response.json()['nft']


async def get_opensea_listings(collection: str) -> dict:
    """Gets the listings of an NFT collection in opensea.
    
    Parameters
    ----------
    collection : string
        Opensea collection slug.

    """
    url = f"https://api.opensea.io/v2/listings/collection/{collection}/all"
    response = await HunterAPI.get(url)
    content = response.json()
    listings = content['listings']
    
    while "next" in content:
        response = await HunterAPI.get(url, {"next": content["next"]})
        content = response.json()
        listings += content['listings']

    return sorted(listings, key=lambda l: float(l['price']['current']['value'])/1e18)