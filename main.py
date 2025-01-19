from dotenv import load_dotenv
from src.client import client
import os

def main():
    load_dotenv()
    GET_TK = os.getenv("DC_TK")
    bot = client.client()
    bot.run(
        reconnect=True,
        token=GET_TK
    )

if __name__=="__main__":
    main()
