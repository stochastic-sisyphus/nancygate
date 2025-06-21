#!/usr/bin/env python3
"""
Database setup for NancyGate with deduplication and source tracking.
Supports both PostgreSQL and SQLite.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib
import json
from pathlib import Path


class NancyGateDB:
    """Database manager for NancyGate trades."""
    
    def __init__(self):
        self.db_type = os.environ.get('DB_TYPE', 'postgresql').lower()
        self.connection = None
        self.setup_database()
    
    def get_connection(self):
        """Get database connection based on DB_TYPE."""
        if self.db_type == 'sqlite':
            db_path = os.environ.get('DB_NAME', 'nancygate.db')
            return sqlite3.connect(db_path)
        else:
            # PostgreSQL
            return psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', 5432),
                database=os.environ.get('DB_NAME', 'nancygate'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', '')
            )
    
    def setup_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        if self.db_type == 'sqlite':
            # SQLite version
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    trade_hash TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    member TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount REAL,
                    date_traded TEXT NOT NULL,
                    date_filed TEXT,
                    date_reported TEXT,
                    description TEXT,
                    
                    -- Signal fields
                    signal_score INTEGER DEFAULT 0,
                    signals TEXT,
                    signal_details TEXT,
                    
                    -- News enrichment fields
                    news_link TEXT,
                    article_title TEXT,
                    published_date TEXT,
                    news_signals TEXT,
                    
                    -- Market data fields
                    price_before REAL,
                    price_after REAL,
                    volume_ratio REAL,
                    
                    -- Metadata
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Create unique constraint for deduplication
                    UNIQUE(member, ticker, transaction_type, date_traded)
                );
            """)
            
            # Create indexes for SQLite
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades(ticker);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_member ON trades(member);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_date ON trades(date_traded);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_signal_score ON trades(signal_score DESC);")
            
            # Create source logs table for SQLite
            cur.execute("""
                CREATE TABLE IF NOT EXISTS source_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL UNIQUE,
                    last_fetch TEXT NOT NULL,
                    total_fetched INTEGER DEFAULT 0,
                    rate_limit_reset TEXT,
                    status TEXT DEFAULT 'active',
                    error_count INTEGER DEFAULT 0,
                    last_error TEXT
                );
            """)
            
            # Create news cache table for SQLite
            cur.execute("""
                CREATE TABLE IF NOT EXISTS news_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    query_date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    articles TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ticker, query_date, source)
                );
            """)
            
        else:
            # PostgreSQL version (original)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    trade_hash VARCHAR(64) PRIMARY KEY,
                    source VARCHAR(50) NOT NULL,
                    member VARCHAR(255) NOT NULL,
                    ticker VARCHAR(10) NOT NULL,
                    transaction_type VARCHAR(20) NOT NULL,
                    amount DECIMAL(15,2),
                    date_traded DATE NOT NULL,
                    date_filed DATE,
                    date_reported DATE,
                    description TEXT,
                    
                    -- Signal fields
                    signal_score INTEGER DEFAULT 0,
                    signals TEXT,
                    signal_details JSONB,
                    
                    -- News enrichment fields
                    news_link TEXT,
                    article_title TEXT,
                    published_date TIMESTAMP,
                    news_signals TEXT,
                    
                    -- Market data fields
                    price_before DECIMAL(10,2),
                    price_after DECIMAL(10,2),
                    volume_ratio DECIMAL(10,2),
                    
                    -- Metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Create unique index for deduplication
                    UNIQUE(member, ticker, transaction_type, date_traded)
                );
                
                CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades(ticker);
                CREATE INDEX IF NOT EXISTS idx_trades_member ON trades(member);
                CREATE INDEX IF NOT EXISTS idx_trades_date ON trades(date_traded);
                CREATE INDEX IF NOT EXISTS idx_trades_signal_score ON trades(signal_score DESC);
            """)
            
            # Create source logs table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS source_logs (
                    id SERIAL PRIMARY KEY,
                    source VARCHAR(50) NOT NULL,
                    last_fetch TIMESTAMP NOT NULL,
                    total_fetched INTEGER DEFAULT 0,
                    rate_limit_reset TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active',
                    error_count INTEGER DEFAULT 0,
                    last_error TEXT,
                    UNIQUE(source)
                );
            """)
            
            # Create news enrichment cache
            cur.execute("""
                CREATE TABLE IF NOT EXISTS news_cache (
                    id SERIAL PRIMARY KEY,
                    ticker VARCHAR(10) NOT NULL,
                    query_date DATE NOT NULL,
                    source VARCHAR(20) NOT NULL,
                    articles JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ticker, query_date, source)
                );
            """)
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Database tables created successfully ({self.db_type})")
    
    def generate_trade_hash(self, trade: Dict[str, Any]) -> str:
        """Generate unique hash for trade deduplication"""
        key_parts = [
            str(trade.get('member', '')),
            str(trade.get('ticker', '')),
            str(trade.get('transaction_type', '')),
            str(trade.get('date_traded', ''))
        ]
        return hashlib.sha256('|'.join(key_parts).encode()).hexdigest()
    
    def insert_trade(self, trade: Dict[str, Any], source: str) -> bool:
        """Insert trade with deduplication"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        trade_hash = self.generate_trade_hash(trade)
        
        try:
            if self.db_type == 'sqlite':
                # SQLite version with ? placeholders
                cur.execute("""
                    INSERT OR REPLACE INTO trades (
                        trade_hash, source, member, ticker, transaction_type,
                        amount, date_traded, date_filed, date_reported, description,
                        signal_score, signals, signal_details
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trade_hash,
                    source,
                    trade.get('member', trade.get('Name', trade.get('Representative', ''))),
                    trade.get('ticker', trade.get('Ticker', '')),
                    trade.get('transaction_type', trade.get('Transaction', '')),
                    trade.get('amount', trade.get('Amount', 0)),
                    trade.get('date_traded', trade.get('Traded')),
                    trade.get('date_filed', trade.get('Filed')),
                    trade.get('date_reported', trade.get('Reported')),
                    trade.get('description', trade.get('Description', '')),
                    trade.get('signal_score', 0),
                    trade.get('signals', ''),
                    json.dumps(trade.get('signal_details', {}))
                ))
            else:
                # PostgreSQL version with %s placeholders
                cur.execute("""
                    INSERT INTO trades (
                        trade_hash, source, member, ticker, transaction_type,
                        amount, date_traded, date_filed, date_reported, description,
                        signal_score, signals, signal_details
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) ON CONFLICT (member, ticker, transaction_type, date_traded) 
                    DO UPDATE SET
                        updated_at = CURRENT_TIMESTAMP,
                        signal_score = GREATEST(trades.signal_score, EXCLUDED.signal_score),
                        signals = CASE 
                            WHEN trades.signals IS NULL THEN EXCLUDED.signals
                            ELSE trades.signals || ',' || EXCLUDED.signals
                        END
                    RETURNING trade_hash;
                """, (
                    trade_hash,
                    source,
                    trade.get('member', trade.get('Name', trade.get('Representative', ''))),
                    trade.get('ticker', trade.get('Ticker', '')),
                    trade.get('transaction_type', trade.get('Transaction', '')),
                    trade.get('amount', trade.get('Amount', 0)),
                    trade.get('date_traded', trade.get('Traded')),
                    trade.get('date_filed', trade.get('Filed')),
                    trade.get('date_reported', trade.get('Reported')),
                    trade.get('description', trade.get('Description', '')),
                    trade.get('signal_score', 0),
                    trade.get('signals', ''),
                    json.dumps(trade.get('signal_details', {}))
                ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error inserting trade: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    def update_source_log(self, source: str, fetched_count: int):
        """Update source fetch timestamp"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        if self.db_type == 'sqlite':
            cur.execute("""
                INSERT OR REPLACE INTO source_logs (source, last_fetch, total_fetched)
                VALUES (?, ?, ?)
            """, (source, datetime.now().isoformat(), fetched_count))
        else:
            cur.execute("""
                INSERT INTO source_logs (source, last_fetch, total_fetched)
                VALUES (%s, %s, %s)
                ON CONFLICT (source) DO UPDATE SET
                    last_fetch = EXCLUDED.last_fetch,
                    total_fetched = source_logs.total_fetched + EXCLUDED.total_fetched;
            """, (source, datetime.now(), fetched_count))
        
        conn.commit()
        cur.close()
        conn.close()
    
    def get_trades_for_enrichment(self, limit: int = 100):
        """Get trades that need news enrichment"""
        conn = self.get_connection()
        trades = []
        
        if self.db_type == 'sqlite':
            # SQLite version
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM trades 
                WHERE news_link IS NULL 
                AND ticker != ''
                ORDER BY date_traded DESC
                LIMIT ?;
            """, (limit,))
            
            # Fetch and convert to dict format
            columns = [description[0] for description in cur.description]
            rows = cur.fetchall()
            trades = [dict(zip(columns, row)) for row in rows]
        else:
            # PostgreSQL version
            from psycopg2.extras import RealDictCursor
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT * FROM trades 
                WHERE news_link IS NULL 
                AND ticker != ''
                ORDER BY date_traded DESC
                LIMIT %s;
            """, (limit,))
            trades = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return trades
    
    def update_trade_enrichment(self, trade_hash: str, enrichment_data: Dict[str, Any]):
        """Update trade with enrichment data"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        if self.db_type == 'sqlite':
            cur.execute("""
                UPDATE trades SET
                    news_link = ?,
                    article_title = ?,
                    published_date = ?,
                    news_signals = ?,
                    signal_score = signal_score + ?,
                    signals = CASE 
                        WHEN signals = '' THEN ?
                        ELSE signals || ',' || ?
                    END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE trade_hash = ?;
            """, (
                enrichment_data.get('news_link'),
                enrichment_data.get('article_title'),
                enrichment_data.get('published_date'),
                enrichment_data.get('news_signals'),
                enrichment_data.get('score_delta', 0),
                enrichment_data.get('new_signals', ''),
                enrichment_data.get('new_signals', ''),
                trade_hash
            ))
        else:
            cur.execute("""
                UPDATE trades SET
                    news_link = %s,
                    article_title = %s,
                    published_date = %s,
                    news_signals = %s,
                    signal_score = signal_score + %s,
                    signals = CASE 
                        WHEN signals = '' THEN %s
                        ELSE signals || ',' || %s
                    END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE trade_hash = %s;
            """, (
                enrichment_data.get('news_link'),
                enrichment_data.get('article_title'),
                enrichment_data.get('published_date'),
                enrichment_data.get('news_signals'),
                enrichment_data.get('score_delta', 0),
                enrichment_data.get('new_signals', ''),
                enrichment_data.get('new_signals', ''),
                trade_hash
            ))
        
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Set up database
    db = NancyGateDB()
    print("✅ Database setup complete!") 