<<<<<<< HEAD
# Smart Research System - Backend

This is the backend for the **Smart Research System**, built using FastAPI and Python. It acts as the bridge between the academic literature database (IEEE Xplore) and a Large Language Model (Groq / Llama-3.3-70b-versatile).

## Features

- **IEEE Integration:** Fetches real-time academic papers using the IEEE API.
- **AI Analysis:** Uses LLM via Groq to analyze academic abstracts and categorize them conceptually.
- **Intelligent Categorization:** Sorts papers into:
  1. Foundational Work (Past Research)
  2. Active Development (Ongoing Research)
  3. Emerging (Future Scope)
- **Rate Limiting:** Built-in endpoint protection using `slowapi` to prevent abuse.
- **CORS Configured:** Pre-configured for Vite frontend origins.

## Tech Stack

- **Framework:** FastAPI
- **Server:** Uvicorn
- **AI Engine:** Groq API (`llama-3.3-70b-versatile`)
- **HTTP Client:** HTTPX (for async IEEE API requests)
- **Rate Limiter:** SlowAPI

## Prerequisites

- Python 3.9+
- An IEEE API Key
- A Groq API Key

## Setup & Running

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root of the backend directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   IEEE_API_KEY=your_ieee_api_key_here
   ```

4. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## API Documentation

FastAPI auto-generates interactive API documentation. Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
=======
# smart-research-backend
>>>>>>> cd04a63fde2c249d2cace74e65bccffe0da5c921
