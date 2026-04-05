import os
from dotenv import load_dotenv

load_dotenv()

IEEE_API_KEY = os.getenv("IEEE_API_KEY")
IEEE_BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
