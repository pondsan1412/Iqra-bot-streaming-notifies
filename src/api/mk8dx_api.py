import requests
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

def stats_mmr_and_ranked(user_id: int):
    """
    user_id must be discord.Member ID
    This function returns 2 values:
    1. mmr
    2. ranked
    """
    API = os.getenv("MK8DX_USER_INFO_DETAILS")
    if not API:
        raise ValueError("API endpoint is not defined. Check your .env file or environment variables.")
    
    response = requests.get(f"{API}{user_id}")
    if response.status_code == 200:
        try:
            data = response.json()  # Parse JSON response
            mmr = data.get("mmr")  # Extract MMR
            ranked = data.get("overallRank")  # Extract Ranked
            name = data.get("name")
            rank = data.get("rank")
            season = data.get("season")
            return mmr, ranked, name, rank
        except ValueError as e:
            raise ValueError("Failed to parse JSON response.") from e
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
def batch_stats_mmr_and_ranked(user_ids: list[int]):
    """
    Fetch MMR and rank for multiple users in a single API call.
    user_ids: List of discord.Member IDs
    """
    API = os.getenv("MK8DX_USER_INFO_DETAILS")
    if not API:
        raise ValueError("API endpoint is not defined. Check your .env file or environment variables.")
    
    response = requests.get(f"{API}", params={"ids": ",".join(map(str, user_ids))})
    if response.status_code == 200:
        try:
            return response.json()  # Return parsed JSON data
        except ValueError as e:
            raise ValueError("Failed to parse JSON response.") from e
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
async def async_stats_mmr_and_ranked(user_id: int):
    """
    Asynchronous function to fetch MMR, name, and rank of a user.
    """
    API = os.getenv("MK8DX_USER_INFO_DETAILS")
    if not API:
        raise ValueError("API endpoint is not defined. Check your .env file or environment variables.")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API}{user_id}") as response:
            if response.status == 200:
                data = await response.json()
                mmr = data.get("mmr", "N/A")
                name = data.get("name", "Unknown")
                rank = data.get("rank", "N/A")
                season = data.get("season", "N/A")
                return mmr, name, rank, season



class NoDataError(Exception):
    """Custom exception for no data available."""
    pass

async def previous_season_stats(user_id: int, season: int=None):
    """
    Fetch MMR and rank of a user from a previous season.
    """
    API = os.getenv("MK8DX_USER_INFO_DETAILS")
    if not API:
        raise ValueError("API endpoint is not defined. Check your .env file or environment variables.")
    
    try:
        if season is None:
            season = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API}{user_id}&season={season}") as response:
                if response.status == 200:
                    data = await response.json()
                    if not data or "errors" in data and "season" in data["errors"]:
                        raise NoDataError(f"Player {user_id} has not played in season {season} yet or the season is invalid.")
                    mmr = data.get("mmr", "N/A")
                    name = data.get("name", "Unknown")
                    rank = data.get("rank", "N/A")
                    season = data.get("season", "N/A")
                    return mmr, name, rank, season
                else:
                    raise Exception(f"This user has not played in season {season} yet")
    except aiohttp.ClientError as e:
        raise Exception(f"{e}")
    except Exception as e:
        raise Exception(f"{e}")