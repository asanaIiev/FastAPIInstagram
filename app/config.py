import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_LIFETIME = 30
REFRESH_TOKEN_LIFETIME = 7
ALGORITHM = 'HS256'