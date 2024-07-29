import os
from dotenv import load_dotenv
load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
RATE_LIMIT_DURATION = os.getenv("RATE_LIMIT_DURATION")
RATE_LIMIT_MAX_REQUESTS = os.getenv("RATE_LIMIT_MAX_REQUESTS")
TEST_USER_ID = os.getenv("TEST_USER_ID")