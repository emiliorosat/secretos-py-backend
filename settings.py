from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

jwtSecret = os.getenv("JWT_SECRET")


