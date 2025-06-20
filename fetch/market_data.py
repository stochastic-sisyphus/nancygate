"""Market data fetcher using Polygon.io and other sources."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import yfinance as yf
import time

from config import Settings


class MarketDataFetcher:
    """Fetches market data for price and volume validation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.polygon_key = self.settings.get('POLYGON_API_KEY')
        self.polygon_base = "https://api.polygon.io"
        
    def fetch_ticker_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        use_polygon: bool = True
    ) -> pd.DataFrame:
        """
        Fetch price and volume data for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data
            end_date: End date for data
            use_polygon: Use Polygon.io if available, else Yahoo Finance
            
        Returns:
            DataFrame with OHLCV data
        """
        if use_polygon and self.polygon_key:
            return self._fetch_polygon_data(ticker, start_date, end_date)
        else:
            return self._fetch_yahoo_data(ticker, start_date, end_date)
    
    def _fetch_polygon_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Fetch data from Polygon.io."""
        endpoint = f"{self.polygon_base}/v2/aggs/ticker/{ticker}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
        
        params = {
            'apiKey': self.polygon_key,
            'adjusted': 'true',
            'sort': 'asc',
            'limit': 50000
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' in data and data['results']:
                df = pd.DataFrame(data['results'])
                
                # Rename columns to standard format
                df = df.rename(columns={
                    'o': 'Open',
                    'h': 'High',
                    'l': 'Low',
                    'c': 'Close',
                    'v': 'Volume',
                    't': 'Timestamp',
                    'vw': 'VWAP',
                    'n': 'Transactions'
                })
                
                # Convert timestamp to datetime
                df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
                df = df.set_index('Date')
                
                print(f"  ✓ Retrieved {len(df)} days of data for {ticker} from Polygon")
                return df
                
        except Exception as e:
            print(f"  ⚠️ Polygon error for {ticker}: {e}")
            print("  ↳ Falling back to Yahoo Finance")
            
        return self._fetch_yahoo_data(ticker, start_date, end_date)
    
    def _fetch_yahoo_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Fetch data from Yahoo Finance as fallback."""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            if not df.empty:
                # Add VWAP calculation
                df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
                print(f"  ✓ Retrieved {len(df)} days of data for {ticker} from Yahoo")
                return df
            
        except Exception as e:
            print(f"  ❌ Yahoo error for {ticker}: {e}")
            
        return pd.DataFrame()
    
    def validate_trade_timing(
        self,
        trades_df: pd.DataFrame,
        days_before: int = 3,
        days_after: int = 3
    ) -> pd.DataFrame:
        """
        Validate trades against market movements.
        
        Adds columns:
        - PriceChangeBefore: Price change % in days before trade
        - PriceChangeAfter: Price change % in days after trade
        - VolumeSpikeBefore: Volume spike detected before trade
        - MarketTiming: 'BOTTOM', 'TOP', or 'NEUTRAL'
        """
        print("\n📈 Validating trades against market data...")
        
        trades_df['PriceChangeBefore'] = 0.0
        trades_df['PriceChangeAfter'] = 0.0
        trades_df['VolumeSpikeBefore'] = False
        trades_df['VolumeAnomalyScore'] = 0.0
        trades_df['MarketTiming'] = 'NEUTRAL'
        
        # Process each unique ticker
        tickers = trades_df['Ticker'].dropna().unique()
        ticker_data = {}
        
        # Fetch data for all tickers first
        for ticker in tickers[:50]:  # Limit for MVP
            if pd.isna(ticker) or ticker == '':
                continue
                
            # Get date range from trades
            ticker_trades = trades_df[trades_df['Ticker'] == ticker]
            if 'Traded' not in ticker_trades.columns:
                continue
                
            min_date = ticker_trades['Traded'].min() - timedelta(days=days_before+10)
            max_date = ticker_trades['Traded'].max() + timedelta(days=days_after+10)
            
            if pd.isna(min_date) or pd.isna(max_date):
                continue
            
            print(f"  📊 Fetching data for {ticker}...")
            market_data = self.fetch_ticker_data(ticker, min_date, max_date)
            
            if not market_data.empty:
                ticker_data[ticker] = market_data
            
            time.sleep(0.1)  # Rate limiting
        
        # Validate each trade
        validated_count = 0
        
        for idx, trade in trades_df.iterrows():
            ticker = trade.get('Ticker')
            trade_date = trade.get('Traded')
            transaction_type = trade.get('Transaction', '')
            
            if ticker not in ticker_data or pd.isna(trade_date):
                continue
            
            market_data = ticker_data[ticker]
            
            # Find closest trading day
            closest_date = self._find_closest_trading_day(trade_date, market_data.index)
            if closest_date is None:
                continue
            
            # Calculate price changes
            before_date = closest_date - timedelta(days=days_before)
            after_date = closest_date + timedelta(days=days_after)
            
            # Price change before trade
            if before_date in market_data.index and closest_date in market_data.index:
                price_before = market_data.loc[before_date, 'Close']
                price_on_date = market_data.loc[closest_date, 'Close']
                price_change_before = ((price_on_date - price_before) / price_before) * 100
                trades_df.at[idx, 'PriceChangeBefore'] = round(price_change_before, 2)
            
            # Price change after trade
            if closest_date in market_data.index and after_date in market_data.index:
                price_on_date = market_data.loc[closest_date, 'Close']
                price_after = market_data.loc[after_date, 'Close']
                price_change_after = ((price_after - price_on_date) / price_on_date) * 100
                trades_df.at[idx, 'PriceChangeAfter'] = round(price_change_after, 2)
            
            # Volume analysis
            volume_score = self._analyze_volume_anomaly(
                market_data, 
                closest_date, 
                days_before
            )
            trades_df.at[idx, 'VolumeAnomalyScore'] = volume_score
            trades_df.at[idx, 'VolumeSpikeBefore'] = volume_score > 2.0
            
            # Market timing classification
            timing = self._classify_market_timing(
                price_change_before,
                price_change_after,
                transaction_type
            )
            trades_df.at[idx, 'MarketTiming'] = timing
            
            validated_count += 1
        
        print(f"  ✓ Validated {validated_count} trades against market data")
        
        # Add market timing signals
        perfect_timing = trades_df['MarketTiming'].isin(['BOTTOM_BUY', 'TOP_SELL'])
        trades_df.loc[perfect_timing, 'SignalScore'] = trades_df.loc[perfect_timing, 'SignalScore'] + 5
        trades_df.loc[perfect_timing, 'Signals'] = trades_df.loc[perfect_timing, 'Signals'] + 'MARKET_TIMING,'
        
        volume_spike = trades_df['VolumeSpikeBefore'] == True
        trades_df.loc[volume_spike, 'SignalScore'] = trades_df.loc[volume_spike, 'SignalScore'] + 3
        trades_df.loc[volume_spike, 'Signals'] = trades_df.loc[volume_spike, 'Signals'] + 'VOLUME_SPIKE,'
        
        return trades_df
    
    def _find_closest_trading_day(
        self,
        target_date: datetime,
        trading_days: pd.DatetimeIndex
    ) -> Optional[datetime]:
        """Find the closest trading day to target date."""
        if len(trading_days) == 0:
            return None
        
        # Find the closest date
        deltas = abs(trading_days - target_date)
        closest_idx = deltas.argmin()
        closest_date = trading_days[closest_idx]
        
        # Only return if within 5 days
        if abs((closest_date - target_date).days) <= 5:
            return closest_date
        
        return None
    
    def _analyze_volume_anomaly(
        self,
        market_data: pd.DataFrame,
        trade_date: datetime,
        lookback_days: int
    ) -> float:
        """
        Calculate volume anomaly score.
        
        Returns:
            Score indicating how unusual the volume is (0-10)
        """
        try:
            # Get volume data around trade date
            start = trade_date - timedelta(days=lookback_days+20)
            end = trade_date
            
            volume_window = market_data.loc[start:end, 'Volume']
            
            if len(volume_window) < 10:
                return 0.0
            
            # Calculate rolling statistics
            mean_volume = volume_window[:-lookback_days].mean()
            std_volume = volume_window[:-lookback_days].std()
            
            # Get recent volumes
            recent_volumes = volume_window[-lookback_days:]
            
            if std_volume == 0:
                return 0.0
            
            # Calculate z-scores
            z_scores = (recent_volumes - mean_volume) / std_volume
            max_z_score = z_scores.max()
            
            # Convert to 0-10 scale
            anomaly_score = min(max_z_score, 10.0)
            
            return round(anomaly_score, 2)
            
        except Exception:
            return 0.0
    
    def _classify_market_timing(
        self,
        price_change_before: float,
        price_change_after: float,
        transaction_type: str
    ) -> str:
        """
        Classify the market timing of a trade.
        
        Returns:
            'BOTTOM_BUY', 'TOP_SELL', 'CONTRARIAN', or 'NEUTRAL'
        """
        is_buy = transaction_type.lower() in ['purchase', 'buy']
        
        # Perfect timing scenarios
        if is_buy and price_change_before < -5 and price_change_after > 5:
            return 'BOTTOM_BUY'
        elif not is_buy and price_change_before > 5 and price_change_after < -5:
            return 'TOP_SELL'
        
        # Contrarian (bad timing)
        elif is_buy and price_change_before > 5 and price_change_after < -5:
            return 'CONTRARIAN'
        elif not is_buy and price_change_before < -5 and price_change_after > 5:
            return 'CONTRARIAN'
        
        return 'NEUTRAL'
    
    def get_sector_performance(
        self,
        sectors: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Get performance data for sector ETFs.
        
        Args:
            sectors: List of sector names
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with sector performance
        """
        # Map sectors to ETFs
        sector_etfs = {
            'Technology': 'XLK',
            'Healthcare': 'XLV',
            'Financial': 'XLF',
            'Energy': 'XLE',
            'Consumer': 'XLY',
            'Industrial': 'XLI',
            'Materials': 'XLB',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Communications': 'XLC'
        }
        
        sector_data = []
        
        for sector, etf in sector_etfs.items():
            if sector not in sectors and sectors != ['all']:
                continue
                
            print(f"  📊 Fetching {sector} sector data ({etf})...")
            
            data = self.fetch_ticker_data(etf, start_date, end_date, use_polygon=False)
            
            if not data.empty:
                performance = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                
                sector_data.append({
                    'Sector': sector,
                    'ETF': etf,
                    'StartPrice': data['Close'].iloc[0],
                    'EndPrice': data['Close'].iloc[-1],
                    'Performance': round(performance, 2),
                    'AvgVolume': data['Volume'].mean()
                })
        
        return pd.DataFrame(sector_data) 