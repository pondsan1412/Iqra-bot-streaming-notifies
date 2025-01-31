import json
from src.api import mk8dx_api

    
import asyncio
run = asyncio.run(mk8dx_api.previous_season_stats(365248485202722818, 4))
print(run)