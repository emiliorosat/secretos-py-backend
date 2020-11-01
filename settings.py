from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

print(os.environ.keys())


jwtSecret = os.environ("JWT_SECRET")

if(jwtSecret == None):
    jwtSecret = os.getenv("JWT_SECRET")

