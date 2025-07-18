import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class AnimeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'AnimeScraperBot/1.0 (Educational Project)'
        }
        self.mal_base_url = 'https://myanimelist.net'
        self.anilist_base_url = 'https://graphql.anilist.co'
        self.cache_file = 'anime_data_cache.json'

    def _make_request(self, url: str, delay: int = 2) -> requests.Response:
        """Make an HTTP request with rate limiting"""
        time.sleep(delay)  # Respect rate limiting
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"Error making request to {url}: {str(e)}")
            raise

    def scrape_myanimelist(self) -> List[Dict]:
        """Scrape top 100 anime from MyAnimeList"""
        logging.info("Starting MyAnimeList scraping...")
        anime_list = []
        
        try:
            # MyAnimeList uses pagination, we'll need multiple requests
            for page in range(0, 4):  # 0-3 to get top 100 (25 per page)
                url = f"{self.mal_base_url}/topanime.php?limit={page * 25}"
                response = self._make_request(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract anime data from the page
                anime_entries = soup.select('tr.ranking-list')
                
                for entry in anime_entries:
                    try:
                        title_tag = entry.select_one('h3.fl-l.fs14.fw-b.anime_ranking_h3')
                        members_tag = entry.select_one('td.pb24 span.text-muted')
                        score_tag = entry.select_one('td.score.ac.fs14')
                        
                        anime_data = {
                            'title': title_tag.text.strip() if title_tag else None,
                            'members': int(members_tag.text.strip().replace(',', '')) if members_tag else None,
                            'score': float(score_tag.text.strip()) if score_tag else None,
                            'source': 'myanimelist'
                        }
                        anime_list.append(anime_data)
                        
                    except Exception as e:
                        logging.error(f"Error parsing anime entry: {str(e)}")
                        continue
                        
        except Exception as e:
            logging.error(f"Error scraping MyAnimeList: {str(e)}")
            
        return anime_list

    def scrape_anilist(self) -> List[Dict]:
        """Scrape top 100 anime from AniList using GraphQL API"""
        logging.info("Starting AniList scraping...")
        anime_list = []
        
        query = """
        query ($page: Int) {
            Page(page: $page, perPage: 50) {
                media(sort: POPULARITY_DESC, type: ANIME) {
                    title {
                        romaji
                        english
                    }
                    popularity
                    averageScore
                }
            }
        }
        """
        
        try:
            for page in range(1, 3):  # 2 pages of 50 to get top 100
                variables = {'page': page}
                response = requests.post(
                    self.anilist_base_url,
                    json={'query': query, 'variables': variables},
                    headers=self.headers
                )
                response.raise_for_status()
                
                data = response.json()
                media_list = data['data']['Page']['media']
                
                for media in media_list:
                    anime_data = {
                        'title': media['title']['english'] or media['title']['romaji'],
                        'members': media['popularity'],
                        'score': media['averageScore'] / 10 if media['averageScore'] else None,
                        'source': 'anilist'
                    }
                    anime_list.append(anime_data)
                    
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            logging.error(f"Error scraping AniList: {str(e)}")
            
        return anime_list

    def merge_and_sort_data(self, mal_data: List[Dict], anilist_data: List[Dict]) -> List[Dict]:
        """Merge and sort data from both sources"""
        all_anime = mal_data + anilist_data
        # Sort by member count (popularity) in descending order
        return sorted(all_anime, key=lambda x: x['members'], reverse=True)

    def save_to_json(self, data: List[Dict]) -> None:
        """Save scraped data to JSON file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_updated': datetime.utcnow().isoformat(),
                    'anime_data': data
                }, f, ensure_ascii=False, indent=2)
            logging.info(f"Data successfully saved to {self.cache_file}")
        except Exception as e:
            logging.error(f"Error saving data to JSON: {str(e)}")

def main():
    scraper = AnimeScraper()
    
    # Scrape data from both sources
    mal_data = scraper.scrape_myanimelist()
    anilist_data = scraper.scrape_anilist()
    
    # Merge and sort the data
    combined_data = scraper.merge_and_sort_data(mal_data, anilist_data)
    
    # Save the results
    scraper.save_to_json(combined_data)
    
    logging.info(f"Scraping completed. Total anime collected: {len(combined_data)}")

if __name__ == "__main__":
    main()
