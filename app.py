from flask import Flask, render_template, jsonify
from database import AnimeDatabase
from main import AnimeScraper
import logging
from config import WEB_CONFIG, LOG_CONFIG

app = Flask(__name__)
db = AnimeDatabase()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/anime')
def get_anime():
    """API endpoint to get anime data"""
    anime_list = db.get_top_anime()
    return jsonify(anime_list)

@app.route('/api/update', methods=['POST'])
def update_data():
    """Endpoint to trigger data update"""
    try:
        scraper = AnimeScraper()
        mal_data = scraper.scrape_myanimelist()
        anilist_data = scraper.scrape_anilist()
        combined_data = scraper.merge_and_sort_data(mal_data, anilist_data)
        db.insert_anime(combined_data)
        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(
        host=WEB_CONFIG['host'],
        port=WEB_CONFIG['port'],
        debug=WEB_CONFIG['debug']
    )
