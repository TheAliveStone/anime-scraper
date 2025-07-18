# Anime Data Scraper

A web application that scrapes and displays the top 100 most popular anime from MyAnimeList and AniList.

## Features

- Scrapes data from MyAnimeList and AniList
- Displays combined rankings with member counts and scores
- Interactive web interface with charts and filtering
- Regular data updates
- Caching system to minimize API requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TheAliveStone/anime-scraper.git
cd anime-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `main.py` - Main scraping logic
- `app.py` - Flask web application
- `database.py` - Database operations
- `config.py` - Configuration settings
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `data/` - Stored data and logs

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details.

## Disclaimer

This project is for educational purposes only. Please respect the terms of service of MyAnimeList and AniList when using this application.
