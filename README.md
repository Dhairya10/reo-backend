
# Reo

Reo is a tool for managing video content filtering

## Features

- User authentication and profile management with Supabase
- Video content filtering based on user preferences

## Demo

You can try out the demo [here](https://reokids.replit.app/)

You can find the demo video [here](https://www.loom.com/share/413490209e06468bb124075878509b5d?sid=bb0861d4-da52-4d43-9d16-5aa64ba106ea)

## Getting Started

### Prerequisites

- Python 3.7+
- Supabase account

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
   DB_CONNECTION_STRING=your_postgres_connection_string
   COLLECTION_NAME=your_vector_collection_name
   RATE_LIMIT_DURATION=60
   RATE_LIMIT_MAX_REQUESTS=5
   ```