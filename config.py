from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Data directory for storing scraped data
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Cache directory
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# API Configuration
API_CONFIG = {
    "MAL": {
        "base_url": "https://myanimelist.net",
        "rate_limit": 2,  # seconds between requests
    },
    "ANILIST": {
        "base_url": "https://graphql.anilist.co",
        "rate_limit": 1,
    }
}

# Database Configuration
DB_CONFIG = {
    "filename": str(DATA_DIR / "anime_database.db"),
}

# Logging Configuration
LOG_CONFIG = {
    "filename": str(DATA_DIR / "scraper.log"),
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "level": "INFO",
}

# Web Interface Configuration
WEB_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False,
}
