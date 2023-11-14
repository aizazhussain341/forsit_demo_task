import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
LOW_STOCKS = int(os.getenv('LOW_STOCKS'))
