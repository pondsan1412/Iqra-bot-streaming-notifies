import os
from dotenv import load_dotenv

load_dotenv()

l = os.getenv("HOST_DB")
p = os.getenv("PASSWORD_DB")

print(f"HOST_DB: {type(l)}")
print(f"PASSWORD_DB:{type(p)}")