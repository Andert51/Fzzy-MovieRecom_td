"""
Enhanced Data Loader for Fuzzy Movie Recommendation System

This module provides comprehensive data loading and management capabilities for the
movie recommendation system. It handles multiple data formats, performs intelligent
data validation, and provides utilities for data exploration and quality assessment.

Key Features:
- Support for multiple data formats (CSV, JSON, Excel, SQL databases)
- Intelligent column detection and mapping
- Data quality assessment and cleaning
- Sample data generation for testing
- Data export and backup capabilities
- Integration with external movie databases (TMDb, OMDb, etc.)
"""

import pandas as pd
import numpy as np
import json
import sqlite3
import requests
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass
import warnings
import logging
from datetime import datetime
import os
import re

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataQualityReport:
    """
    Data quality assessment report.
    
    Attributes:
        total_records (int): Total number of records
        valid_records (int): Number of valid records after cleaning
        duplicate_records (int): Number of duplicate records found
        missing_data_summary (Dict[str, int]): Missing data count by column
        data_type_issues (List[str]): List of data type issues found
        quality_score (float): Overall data quality score (0-1)
        recommendations (List[str]): Data quality improvement recommendations
    """
    total_records: int
    valid_records: int
    duplicate_records: int
    missing_data_summary: Dict[str, int]
    data_type_issues: List[str]
    quality_score: float
    recommendations: List[str]


@dataclass
class DataSourceConfig:
    """
    Configuration for data sources.
    
    Attributes:
        source_type (str): Type of data source ('csv', 'json', 'excel', 'sql', 'api')
        source_path (str): Path or URL to data source
        connection_params (Dict[str, Any]): Connection parameters for databases/APIs
        column_mapping (Dict[str, str]): Column name mapping
        preprocessing_options (Dict[str, Any]): Preprocessing options
    """
    source_type: str
    source_path: str
    connection_params: Dict[str, Any]
    column_mapping: Dict[str, str]
    preprocessing_options: Dict[str, Any]


class EnhancedDataLoader:
    """
    Advanced data loading system for movie recommendation engine.
    
    This class provides comprehensive data management capabilities including:
    - Multi-format data loading (CSV, JSON, Excel, SQL)
    - Intelligent data validation and cleaning
    - External API integration for movie data enrichment
    - Data quality assessment and reporting
    - Sample data generation for testing and development
    """
    
    def __init__(self, cache_dir: str = "data_cache", enable_caching: bool = True):
        """
        Initialize the enhanced data loader.
        
        Args:
            cache_dir (str): Directory for caching data
            enable_caching (bool): Whether to enable data caching
        """
        self.cache_dir = Path(cache_dir)
        self.enable_caching = enable_caching
        
        # Create cache directory if it doesn't exist
        if self.enable_caching:
            self.cache_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.loaded_datasets = {}
        self.data_quality_reports = {}
        
        # Configuration
        self.required_columns = ['movie_id', 'title', 'genres', 'actors', 'average_rating']
        self.optional_columns = ['release_year', 'runtime', 'director', 'plot', 'imdb_id']
        
        # Column mapping patterns for automatic detection
        self.column_patterns = {
            'movie_id': [r'id', r'movie_id', r'movieid', r'film_id'],
            'title': [r'title', r'name', r'movie_name', r'film_name'],
            'genres': [r'genre', r'genres', r'category', r'categories'],
            'actors': [r'actor', r'actors', r'cast', r'starring'],
            'average_rating': [r'rating', r'score', r'imdb_rating', r'avg_rating', r'average_rating'],
            'release_year': [r'year', r'release_year', r'release_date'],
            'runtime': [r'runtime', r'duration', r'length'],
            'director': [r'director', r'directors'],
            'plot': [r'plot', r'summary', r'description', r'overview']
        }
        
        logger.info(f"Enhanced Data Loader initialized with caching {'enabled' if enable_caching else 'disabled'}")
    
    def load_data(self, config: DataSourceConfig) -> Tuple[pd.DataFrame, DataQualityReport]:
        """
        Load data from various sources with comprehensive validation.
        
        Args:
            config (DataSourceConfig): Data source configuration
        
        Returns:
            Tuple[pd.DataFrame, DataQualityReport]: Loaded data and quality report
        """
        
        logger.info(f"Loading data from {config.source_type}: {config.source_path}")
        
        try:
            # Load data based on source type
            if config.source_type.lower() == 'csv':
                data = self._load_csv(config)
            elif config.source_type.lower() == 'json':
                data = self._load_json(config)
            elif config.source_type.lower() == 'excel':
                data = self._load_excel(config)
            elif config.source_type.lower() == 'sql':
                data = self._load_sql(config)
            elif config.source_type.lower() == 'api':
                data = self._load_api(config)
            else:
                raise ValueError(f"Unsupported source type: {config.source_type}")
            
            # Apply column mapping
            if config.column_mapping:
                data = data.rename(columns=config.column_mapping)
            
            # Auto-detect columns if mapping not provided
            data = self._auto_detect_columns(data)
            
            # Validate and clean data
            cleaned_data = self._validate_and_clean_data(data)
            
            # Generate quality report
            quality_report = self._generate_quality_report(data, cleaned_data)
            
            # Cache data if enabled
            if self.enable_caching:
                self._cache_data(config, cleaned_data, quality_report)
            
            # Store in memory
            dataset_id = f"{config.source_type}_{hash(config.source_path)}"
            self.loaded_datasets[dataset_id] = cleaned_data
            self.data_quality_reports[dataset_id] = quality_report
            
            logger.info(f"Successfully loaded {len(cleaned_data)} records with quality score: {quality_report.quality_score:.2f}")
            
            return cleaned_data, quality_report
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def create_sample_dataset(self, num_movies: int = 100, 
                            include_ratings: bool = True,
                            genre_distribution: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """
        Create a comprehensive sample movie dataset for testing and development.
        
        Args:
            num_movies (int): Number of movies to generate
            include_ratings (bool): Whether to include user ratings
            genre_distribution (Dict[str, float]): Custom genre distribution
        
        Returns:
            pd.DataFrame: Generated sample dataset
        """
        
        logger.info(f"Creating sample dataset with {num_movies} movies")
        
        # Default genre distribution
        if not genre_distribution:
            genre_distribution = {
                'Action': 0.15, 'Drama': 0.20, 'Comedy': 0.15, 'Thriller': 0.10,
                'Romance': 0.08, 'Horror': 0.07, 'Sci-Fi': 0.08, 'Adventure': 0.10,
                'Crime': 0.07
            }
        
        # Sample movie titles with genres
        movie_templates = [
            # Action movies
            ("The Last Guardian", "Action|Adventure"),
            ("Shadow Strike", "Action|Thriller"),
            ("Steel Warrior", "Action|Sci-Fi"),
            ("Night Hunter", "Action|Crime"),
            ("Phoenix Rising", "Action|Drama"),
            
            # Drama movies
            ("Silent Hearts", "Drama|Romance"),
            ("Broken Dreams", "Drama"),
            ("The Long Road", "Drama|Biography"),
            ("Whispers in Time", "Drama|History"),
            ("Fading Light", "Drama|Family"),
            
            # Comedy movies
            ("Laugh Out Loud", "Comedy"),
            ("Crazy Adventures", "Comedy|Adventure"),
            ("The Funny Side", "Comedy|Romance"),
            ("Mad House", "Comedy|Family"),
            ("Comedy Central", "Comedy"),
            
            # Thriller movies
            ("Dark Secrets", "Thriller|Mystery"),
            ("Edge of Tomorrow", "Thriller|Sci-Fi"),
            ("The Pursuit", "Thriller|Crime"),
            ("Hidden Truth", "Thriller|Drama"),
            ("Final Hour", "Thriller|Action"),
            
            # Horror movies
            ("Nightmare House", "Horror"),
            ("The Haunting", "Horror|Thriller"),
            ("Dark Woods", "Horror|Mystery"),
            ("Blood Moon", "Horror|Supernatural"),
            ("Terror Night", "Horror"),
            
            # Sci-Fi movies
            ("Future World", "Sci-Fi|Adventure"),
            ("Space Odyssey", "Sci-Fi|Drama"),
            ("Cyber Wars", "Sci-Fi|Action"),
            ("Time Paradox", "Sci-Fi|Thriller"),
            ("Alien Contact", "Sci-Fi"),
            
            # Romance movies
            ("Love Story", "Romance|Drama"),
            ("First Kiss", "Romance|Comedy"),
            ("Eternal Love", "Romance"),
            ("Summer Romance", "Romance|Drama"),
            ("Heart's Desire", "Romance")
        ]
        
        # Famous actors pool
        actors_pool = [
            "Leonardo DiCaprio", "Meryl Streep", "Denzel Washington", "Scarlett Johansson",
            "Robert Downey Jr.", "Cate Blanchett", "Tom Hanks", "Charlize Theron",
            "Brad Pitt", "Jennifer Lawrence", "Morgan Freeman", "Emma Stone",
            "Will Smith", "Natalie Portman", "Christian Bale", "Amy Adams",
            "Matt Damon", "Viola Davis", "Ryan Gosling", "Sandra Bullock",
            "Samuel L. Jackson", "Reese Witherspoon", "Hugh Jackman", "Jessica Chastain",
            "Robert De Niro", "Julianne Moore", "Kevin Costner", "Helen Mirren",
            "Mark Wahlberg", "Tilda Swinton", "Jake Gyllenhaal", "Lupita Nyong'o",
            "Chris Evans", "Margot Robbie", "Anthony Hopkins", "Frances McDormand",
            "Ryan Reynolds", "Saoirse Ronan", "Idris Elba", "Brie Larson"
        ]
        
        # Generate sample data
        sample_data = []
        
        for i in range(num_movies):
            # Select random movie template
            title_template, genres = movie_templates[i % len(movie_templates)]
            
            # Modify title to make it unique
            if i >= len(movie_templates):
                title = f"{title_template} {i // len(movie_templates) + 1}"
            else:
                title = title_template
            
            # Select random actors (2-4 actors per movie)
            num_actors = np.random.randint(2, 5)
            selected_actors = np.random.choice(actors_pool, num_actors, replace=False)
            actors_str = "|".join(selected_actors)
            
            # Generate realistic ratings (skewed towards higher ratings)
            rating = np.random.beta(2, 1) * 4 + 6  # Beta distribution scaled to 6-10 range
            rating = round(np.clip(rating, 1.0, 10.0), 1)
            
            # Generate other attributes
            release_year = np.random.randint(1990, 2024)
            runtime = np.random.randint(90, 180)
            
            # Create movie record
            movie_record = {
                'movie_id': f'movie_{i+1:04d}',
                'title': title,
                'genres': genres,
                'actors': actors_str,
                'average_rating': rating,
                'release_year': release_year,
                'runtime': runtime
            }
            
            sample_data.append(movie_record)
        
        # Create DataFrame
        df = pd.DataFrame(sample_data)
        
        # Add some realistic data quality issues for testing
        if num_movies > 50:
            # Add some missing data
            missing_indices = np.random.choice(len(df), size=int(len(df) * 0.02), replace=False)
            df.loc[missing_indices, 'runtime'] = np.nan
            
            # Add some duplicates
            if len(df) > 10:
                duplicate_indices = np.random.choice(len(df), size=min(3, len(df)//20), replace=False)
                for idx in duplicate_indices:
                    df.loc[len(df)] = df.loc[idx].copy()
        
        logger.info(f"Created sample dataset with {len(df)} movies")
        
        return df
    
    def enrich_data_from_api(self, data: pd.DataFrame, api_key: Optional[str] = None) -> pd.DataFrame:
        """
        Enrich movie data using external APIs (TMDb, OMDb, etc.).
        
        Args:
            data (pd.DataFrame): Movie data to enrich
            api_key (str): API key for external services
        
        Returns:
            pd.DataFrame: Enriched movie data
        """
        
        if not api_key:
            logger.warning("No API key provided, skipping data enrichment")
            return data
        
        logger.info(f"Enriching {len(data)} movies with external API data")
        
        enriched_data = data.copy()
        
        # Add placeholder columns for enriched data
        enriched_columns = ['imdb_id', 'plot', 'director', 'budget', 'box_office']
        for col in enriched_columns:
            if col not in enriched_data.columns:
                enriched_data[col] = np.nan
        
        # Simulate API enrichment (in real implementation, would call actual APIs)
        for idx, row in enriched_data.iterrows():
            try:
                # Simulate API delay
                if idx % 10 == 0:
                    logger.info(f"Enriched {idx + 1}/{len(enriched_data)} movies")
                
                # Add simulated enriched data
                enriched_data.at[idx, 'imdb_id'] = f"tt{np.random.randint(1000000, 9999999)}"
                enriched_data.at[idx, 'plot'] = f"An engaging {row['genres'].split('|')[0].lower()} story..."
                enriched_data.at[idx, 'director'] = np.random.choice([
                    "Christopher Nolan", "Steven Spielberg", "Martin Scorsese", "Quentin Tarantino",
                    "Ridley Scott", "David Fincher", "Coen Brothers", "Denis Villeneuve"
                ])
                
                # Limit API calls in demo
                if idx >= 20:  # Only enrich first 20 movies in demo
                    break
                    
            except Exception as e:
                logger.warning(f"Error enriching movie {row['title']}: {e}")
                continue
        
        logger.info("Data enrichment completed")
        
        return enriched_data
    
    def export_data(self, data: pd.DataFrame, output_path: str, 
                   format_type: str = 'csv', include_metadata: bool = True) -> None:
        """
        Export data to various formats with metadata.
        
        Args:
            data (pd.DataFrame): Data to export
            output_path (str): Output file path
            format_type (str): Export format ('csv', 'json', 'excel')
            include_metadata (bool): Whether to include metadata
        """
        
        logger.info(f"Exporting data to {format_type} format: {output_path}")
        
        try:
            if format_type.lower() == 'csv':
                data.to_csv(output_path, index=False)
            elif format_type.lower() == 'json':
                data.to_json(output_path, orient='records', indent=2)
            elif format_type.lower() == 'excel':
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    data.to_excel(writer, sheet_name='Movies', index=False)
                    
                    if include_metadata:
                        # Add metadata sheet
                        metadata = pd.DataFrame({
                            'Property': ['Total Records', 'Export Date', 'Columns', 'Data Types'],
                            'Value': [
                                len(data),
                                datetime.now().isoformat(),
                                ', '.join(data.columns.tolist()),
                                ', '.join([f"{col}:{dtype}" for col, dtype in data.dtypes.items()])
                            ]
                        })
                        metadata.to_excel(writer, sheet_name='Metadata', index=False)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
            
            logger.info(f"Data successfully exported to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    def _load_csv(self, config: DataSourceConfig) -> pd.DataFrame:
        """Load data from CSV file."""
        
        # Check if file exists, create sample if not
        if not Path(config.source_path).exists():
            logger.warning(f"CSV file not found: {config.source_path}. Creating sample data.")
            sample_data = self.create_sample_dataset()
            sample_data.to_csv(config.source_path, index=False)
            return sample_data
        
        # Load CSV with various encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                data = pd.read_csv(config.source_path, encoding=encoding)
                logger.info(f"Successfully loaded CSV with {encoding} encoding")
                return data
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, try with error handling
        try:
            data = pd.read_csv(config.source_path, encoding='utf-8', errors='replace')
            logger.warning("Loaded CSV with character replacement due to encoding issues")
            return data
        except Exception as e:
            raise Exception(f"Failed to load CSV file: {e}")
    
    def _load_json(self, config: DataSourceConfig) -> pd.DataFrame:
        """Load data from JSON file."""
        
        if not Path(config.source_path).exists():
            raise FileNotFoundError(f"JSON file not found: {config.source_path}")
        
        try:
            with open(config.source_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(json_data, list):
                data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                if 'movies' in json_data:
                    data = pd.DataFrame(json_data['movies'])
                elif 'data' in json_data:
                    data = pd.DataFrame(json_data['data'])
                else:
                    # Assume the dict itself contains the data
                    data = pd.DataFrame([json_data])
            else:
                raise ValueError("Unsupported JSON structure")
            
            return data
            
        except Exception as e:
            raise Exception(f"Failed to load JSON file: {e}")
    
    def _load_excel(self, config: DataSourceConfig) -> pd.DataFrame:
        """Load data from Excel file."""
        
        if not Path(config.source_path).exists():
            raise FileNotFoundError(f"Excel file not found: {config.source_path}")
        
        try:
            # Try to load from different sheets
            excel_file = pd.ExcelFile(config.source_path)
            
            # Look for data in common sheet names
            sheet_names = ['Movies', 'Data', 'Sheet1', excel_file.sheet_names[0]]
            
            for sheet_name in sheet_names:
                if sheet_name in excel_file.sheet_names:
                    data = pd.read_excel(config.source_path, sheet_name=sheet_name)
                    logger.info(f"Loaded data from Excel sheet: {sheet_name}")
                    return data
            
            # If no specific sheet found, load the first one
            data = pd.read_excel(config.source_path)
            return data
            
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {e}")
    
    def _load_sql(self, config: DataSourceConfig) -> pd.DataFrame:
        """Load data from SQL database."""
        
        try:
            connection_params = config.connection_params
            
            if 'sqlite' in connection_params.get('engine', '').lower():
                # SQLite connection
                conn = sqlite3.connect(connection_params['database'])
                query = connection_params.get('query', 'SELECT * FROM movies')
                data = pd.read_sql_query(query, conn)
                conn.close()
            else:
                # Other SQL databases (would require additional setup)
                raise NotImplementedError("Non-SQLite databases not implemented in this demo")
            
            return data
            
        except Exception as e:
            raise Exception(f"Failed to load SQL data: {e}")
    
    def _load_api(self, config: DataSourceConfig) -> pd.DataFrame:
        """Load data from API."""
        
        try:
            connection_params = config.connection_params
            
            response = requests.get(
                config.source_path,
                params=connection_params.get('params', {}),
                headers=connection_params.get('headers', {}),
                timeout=connection_params.get('timeout', 30)
            )
            
            response.raise_for_status()
            json_data = response.json()
            
            # Handle different API response structures
            if isinstance(json_data, list):
                data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # Look for common data keys
                data_keys = ['results', 'data', 'movies', 'items']
                for key in data_keys:
                    if key in json_data:
                        data = pd.DataFrame(json_data[key])
                        break
                else:
                    data = pd.DataFrame([json_data])
            else:
                raise ValueError("Unsupported API response structure")
            
            return data
            
        except Exception as e:
            raise Exception(f"Failed to load API data: {e}")
    
    def _auto_detect_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Automatically detect and map column names."""
        
        current_columns = data.columns.tolist()
        column_mapping = {}
        
        for standard_col, patterns in self.column_patterns.items():
            if standard_col in current_columns:
                continue  # Column already correctly named
            
            # Try to find matching column
            for col in current_columns:
                col_lower = col.lower().strip()
                for pattern in patterns:
                    if re.search(pattern, col_lower):
                        column_mapping[col] = standard_col
                        break
                if col in column_mapping:
                    break
        
        if column_mapping:
            logger.info(f"Auto-detected column mappings: {column_mapping}")
            data = data.rename(columns=column_mapping)
        
        return data
    
    def _validate_and_clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the loaded data."""
        
        logger.info("Validating and cleaning data...")
        
        cleaned_data = data.copy()
        
        # Ensure required columns exist
        for col in self.required_columns:
            if col not in cleaned_data.columns:
                if col == 'movie_id':
                    cleaned_data[col] = [f'movie_{i+1:04d}' for i in range(len(cleaned_data))]
                elif col == 'title':
                    cleaned_data[col] = 'Unknown Title'
                elif col == 'genres':
                    cleaned_data[col] = 'Unknown'
                elif col == 'actors':
                    cleaned_data[col] = 'Unknown Actor'
                elif col == 'average_rating':
                    cleaned_data[col] = 5.0
                
                logger.warning(f"Missing required column '{col}' - added default values")
        
        # Remove duplicates
        initial_count = len(cleaned_data)
        cleaned_data = cleaned_data.drop_duplicates(subset=['movie_id'], keep='first')
        duplicates_removed = initial_count - len(cleaned_data)
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate records")
        
        # Clean numeric columns
        numeric_columns = ['average_rating', 'release_year', 'runtime']
        for col in numeric_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
        
        # Validate rating range
        if 'average_rating' in cleaned_data.columns:
            cleaned_data['average_rating'] = cleaned_data['average_rating'].clip(1.0, 10.0)
        
        # Clean string columns
        string_columns = ['title', 'genres', 'actors', 'director', 'plot']
        for col in string_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = cleaned_data[col].astype(str).str.strip()
                # Replace 'nan' strings with actual NaN
                cleaned_data[col] = cleaned_data[col].replace(['nan', 'None', ''], np.nan)
        
        # Remove records with missing critical data
        critical_columns = ['title', 'average_rating']
        for col in critical_columns:
            if col in cleaned_data.columns:
                before_count = len(cleaned_data)
                cleaned_data = cleaned_data.dropna(subset=[col])
                after_count = len(cleaned_data)
                
                if before_count != after_count:
                    logger.info(f"Removed {before_count - after_count} records with missing {col}")
        
        logger.info(f"Data cleaning completed: {len(cleaned_data)} valid records")
        
        return cleaned_data
    
    def _generate_quality_report(self, original_data: pd.DataFrame, 
                               cleaned_data: pd.DataFrame) -> DataQualityReport:
        """Generate comprehensive data quality report."""
        
        # Calculate missing data
        missing_data_summary = {}
        for col in original_data.columns:
            missing_count = original_data[col].isna().sum()
            if missing_count > 0:
                missing_data_summary[col] = int(missing_count)
        
        # Identify data type issues
        data_type_issues = []
        
        # Check rating column
        if 'average_rating' in original_data.columns:
            try:
                pd.to_numeric(original_data['average_rating'], errors='raise')
            except:
                data_type_issues.append("average_rating contains non-numeric values")
        
        # Check for extremely long strings (potential data corruption)
        string_columns = ['title', 'genres', 'actors']
        for col in string_columns:
            if col in original_data.columns:
                max_length = original_data[col].astype(str).str.len().max()
                if max_length > 500:  # Arbitrary threshold
                    data_type_issues.append(f"{col} contains unusually long values (max: {max_length})")
        
        # Calculate quality score
        total_records = len(original_data)
        valid_records = len(cleaned_data)
        duplicate_records = total_records - len(original_data.drop_duplicates())
        
        # Quality score factors
        data_retention_score = valid_records / total_records if total_records > 0 else 0
        missing_data_score = 1 - (sum(missing_data_summary.values()) / (total_records * len(original_data.columns))) if total_records > 0 else 0
        data_type_score = 1 - (len(data_type_issues) / 10)  # Penalize up to 10 issues
        
        quality_score = (data_retention_score * 0.4 + missing_data_score * 0.4 + data_type_score * 0.2)
        quality_score = max(0, min(1, quality_score))  # Ensure 0-1 range
        
        # Generate recommendations
        recommendations = []
        
        if quality_score < 0.7:
            recommendations.append("Consider improving data collection processes")
        
        if missing_data_summary:
            recommendations.append(f"Address missing data in columns: {', '.join(missing_data_summary.keys())}")
        
        if duplicate_records > 0:
            recommendations.append("Implement duplicate detection in data pipeline")
        
        if data_type_issues:
            recommendations.append("Validate data types during data entry")
        
        if quality_score > 0.9:
            recommendations.append("Excellent data quality - consider this dataset as a reference")
        
        return DataQualityReport(
            total_records=total_records,
            valid_records=valid_records,
            duplicate_records=duplicate_records,
            missing_data_summary=missing_data_summary,
            data_type_issues=data_type_issues,
            quality_score=quality_score,
            recommendations=recommendations
        )
    
    def _cache_data(self, config: DataSourceConfig, data: pd.DataFrame, 
                   quality_report: DataQualityReport) -> None:
        """Cache loaded data and quality report."""
        
        try:
            cache_id = f"{config.source_type}_{hash(config.source_path)}"
            
            # Cache data
            data_cache_path = self.cache_dir / f"{cache_id}_data.pkl"
            data.to_pickle(data_cache_path)
            
            # Cache quality report
            report_cache_path = self.cache_dir / f"{cache_id}_report.json"
            report_dict = {
                'total_records': quality_report.total_records,
                'valid_records': quality_report.valid_records,
                'duplicate_records': quality_report.duplicate_records,
                'missing_data_summary': quality_report.missing_data_summary,
                'data_type_issues': quality_report.data_type_issues,
                'quality_score': quality_report.quality_score,
                'recommendations': quality_report.recommendations,
                'cache_timestamp': datetime.now().isoformat()
            }
            
            with open(report_cache_path, 'w') as f:
                json.dump(report_dict, f, indent=2)
            
            logger.info(f"Data cached successfully: {data_cache_path}")
            
        except Exception as e:
            logger.warning(f"Failed to cache data: {e}")
    
    def get_data_summary(self, dataset_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive summary of loaded datasets."""
        
        if dataset_id and dataset_id in self.loaded_datasets:
            datasets = {dataset_id: self.loaded_datasets[dataset_id]}
            reports = {dataset_id: self.data_quality_reports[dataset_id]}
        else:
            datasets = self.loaded_datasets
            reports = self.data_quality_reports
        
        summary = {
            'datasets_loaded': len(datasets),
            'total_records': sum(len(df) for df in datasets.values()),
            'average_quality_score': np.mean([report.quality_score for report in reports.values()]) if reports else 0,
            'datasets': {}
        }
        
        for ds_id, df in datasets.items():
            report = reports.get(ds_id)
            summary['datasets'][ds_id] = {
                'records': len(df),
                'columns': list(df.columns),
                'quality_score': report.quality_score if report else 0,
                'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        
        return summary
    
    def print_data_summary(self) -> None:
        """Print comprehensive data summary."""
        
        summary = self.get_data_summary()
        
        print("="*80)
        print("ENHANCED DATA LOADER - SUMMARY")
        print("="*80)
        
        print(f"\nOverall Statistics:")
        print(f"  • Datasets Loaded: {summary['datasets_loaded']}")
        print(f"  • Total Records: {summary['total_records']}")
        print(f"  • Average Quality Score: {summary['average_quality_score']:.3f}")
        
        if summary['datasets']:
            print(f"\nDataset Details:")
            for ds_id, details in summary['datasets'].items():
                print(f"\n  Dataset: {ds_id}")
                print(f"    • Records: {details['records']}")
                print(f"    • Columns: {len(details['columns'])}")
                print(f"    • Quality Score: {details['quality_score']:.3f}")
                print(f"    • Column Names: {', '.join(details['columns'][:5])}{'...' if len(details['columns']) > 5 else ''}")
        
        print("="*80)


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the enhanced data loader.
    """
    
    print("Enhanced Data Loader for Fuzzy Movie Recommendation System")
    print("=" * 60)
    
    # Initialize data loader
    loader = EnhancedDataLoader(cache_dir="demo_cache", enable_caching=True)
    
    # Create and test sample dataset
    print("\n1. Creating Sample Dataset:")
    print("-" * 40)
    
    sample_data = loader.create_sample_dataset(num_movies=50)
    print(f"Sample dataset created with {len(sample_data)} movies")
    print(f"Columns: {', '.join(sample_data.columns)}")
    
    # Save sample data
    sample_path = "sample_movies_demo.csv"
    sample_data.to_csv(sample_path, index=False)
    
    # Test loading CSV data
    print(f"\n2. Loading CSV Data:")
    print("-" * 40)
    
    config = DataSourceConfig(
        source_type='csv',
        source_path=sample_path,
        connection_params={},
        column_mapping={},
        preprocessing_options={}
    )
    
    loaded_data, quality_report = loader.load_data(config)
    
    print(f"Loaded {len(loaded_data)} records")
    print(f"Data quality score: {quality_report.quality_score:.3f}")
    print(f"Recommendations: {quality_report.recommendations}")
    
    # Test data export
    print(f"\n3. Testing Data Export:")
    print("-" * 40)
    
    loader.export_data(loaded_data, "exported_movies.json", "json")
    loader.export_data(loaded_data, "exported_movies.xlsx", "excel")
    
    # Print summary
    print(f"\n4. Data Loader Summary:")
    print("-" * 40)
    
    loader.print_data_summary()
    
    # Clean up demo files
    try:
        os.remove(sample_path)
        os.remove("exported_movies.json")
        os.remove("exported_movies.xlsx")
        print("\nDemo files cleaned up")
    except:
        pass
