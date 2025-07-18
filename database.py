import sqlite3
from datetime import datetime
from typing import List, Dict
import logging
from config import DB_CONFIG

class AnimeDatabase:
    def __init__(self):
        self.db_path = DB_CONFIG['filename']
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create anime table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anime (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    english_title TEXT,
                    japanese_title TEXT,
                    members INTEGER,
                    score REAL,
                    source TEXT,
                    last_updated TIMESTAMP,
                    mal_id TEXT,
                    anilist_id TEXT
                )
            ''')
            
            # Create genres table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Create anime_genres relationship table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anime_genres (
                    anime_id INTEGER,
                    genre_id INTEGER,
                    FOREIGN KEY (anime_id) REFERENCES anime (id),
                    FOREIGN KEY (genre_id) REFERENCES genres (id),
                    PRIMARY KEY (anime_id, genre_id)
                )
            ''')
            
            conn.commit()

    def insert_anime(self, anime_data: List[Dict]):
        """Insert or update anime data in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for anime in anime_data:
                cursor.execute('''
                    INSERT OR REPLACE INTO anime (
                        title, members, score, source, last_updated
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    anime['title'],
                    anime['members'],
                    anime['score'],
                    anime['source'],
                    datetime.utcnow().isoformat()
                ))
            
            conn.commit()

    def get_top_anime(self, limit: int = 100) -> List[Dict]:
        """Retrieve top anime sorted by member count"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM anime 
                ORDER BY members DESC 
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
