
# Reo API

Reo API is a FastAPI-based backend service for managing a kid-friendly story generation and video content filtering application

## Features

- User authentication and profile management with Supabase
- Story generation using OpenAI's GPT-4o
- Text-to-speech conversion for generated stories using Open AI's TTS API
- Video content filtering based on user preferences

## Getting Started

### Prerequisites

- Python 3.7+
- Supabase account
- OpenAI API key

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/Dhairya10/reo-backend.git
   cd reo-backend
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory and add the following variables:

   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_api_key
   DB_CONNECTION_STRING=your_postgres_connection_string
   COLLECTION_NAME=your_vector_collection_name
   RATE_LIMIT_DURATION=60
   RATE_LIMIT_MAX_REQUESTS=5
   ```

### Running the Application

To run the application locally:
The API will be available at `http://localhost:8000`

## API Endpoints

- `/auth`: User authentication endpoints
- `/stories`: Story generation and retrieval
- `/videos`: Video feed and content filtering
- `/keywords`: Keyword-based content blocking

For detailed API documentation, visit `/docs` when the application is running.

## Project Structure

- `app.py`: Main application entry point
- `routers/`: API route definitions
- `models/`: Pydantic models for data validation
- `services/`: Business logic implementation
- `utils/`: Utility functions and middleware
- `config/`: Configuration and settings