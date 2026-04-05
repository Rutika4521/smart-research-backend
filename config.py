from dotenv import load_dotenv
import os

load_dotenv()

IEEE_API_KEY = os.getenv("IEEE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not IEEE_API_KEY:
    raise RuntimeError("IEEE_API_KEY is not set in .env")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in .env — get a free key at https://console.groq.com")
