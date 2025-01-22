from src.api.twitch_api import TwitchAPI

CLIENT_ID = ""
CLIENT_SECRET = ""

USERNAME = ""

def main():
    twitch = TwitchAPI(CLIENT_ID, CLIENT_SECRET)
    try:
        user_data = twitch.get_user(USERNAME)
        if not user_data:
            print(f"User '{USERNAME}' not found.")
            return
        user_id = user_data[0]["id"]
        print(f"User ID: {user_id}")
        print(f"Display Name: {user_data[0]['display_name']}")

        live_data = twitch.check_live_status(user_id)
        if live_data:
            print(f"{USERNAME} is currently live!")
            print(f"Title: {live_data[0]['title']}")
            print(f"Game: {live_data[0]['game_name']}")
            print(f"Viewers: {live_data[0]['viewer_count']}")
        else:
            print(f"{USERNAME} is not live.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
