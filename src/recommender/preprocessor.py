"""
Data Preprocessing Module for Fuzzy Movie Recommendation System

This module handles the preprocessing and transformation of movie data and user
preferences into the format required by the fuzzy logic system. It includes
functionality for:

- Movie data normalization and cleaning
- User preference analysis and modeling
- Genre matching algorithms
- Actor popularity scoring
- Data validation and quality checks

The preprocessor serves as the bridge between raw movie data and the fuzzy
logic inference engine, ensuring that all inputs are properly scaled and
formatted for optimal recommendation performance.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)


class GenreMatchingStrategy(Enum):
    """Enumeration of genre matching strategies."""
    EXACT_MATCH = "exact_match"
    WEIGHTED_OVERLAP = "weighted_overlap"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    HIERARCHICAL_MATCH = "hierarchical_match"


class ActorPopularitySource(Enum):
    """Enumeration of actor popularity data sources."""
    MOVIE_COUNT = "movie_count"
    RATING_WEIGHTED = "rating_weighted"
    RECENT_ACTIVITY = "recent_activity"
    COMBINED_SCORE = "combined_score"


@dataclass
class UserProfile:
    """
    User preference profile for personalized recommendations.
    
    Attributes:
        user_id (str): Unique user identifier
        rating_history (List[float]): Historical movie ratings
        preferred_genres (Dict[str, float]): Genre preference scores (0-100)
        preferred_actors (Dict[str, float]): Actor preference scores (0-100)
        rating_behavior (Dict[str, float]): Rating behavior characteristics
        last_updated (str): Last profile update timestamp
    """
    user_id: str
    rating_history: List[float]
    preferred_genres: Dict[str, float]
    preferred_actors: Dict[str, float]
    rating_behavior: Dict[str, float]
    last_updated: str


@dataclass
class MovieFeatures:
    """
    Processed movie features for fuzzy logic input.
    
    Attributes:
        movie_id (str): Unique movie identifier
        title (str): Movie title
        genres (List[str]): List of movie genres
        main_actors (List[str]): List of main actors
        average_rating (float): Average user rating
        popularity_score (float): Overall popularity score
        genre_match_score (float): Genre matching score for user
        actor_popularity_score (float): Actor popularity score
        preprocessed_rating (float): Preprocessed user rating input
    """
    movie_id: str
    title: str
    genres: List[str]
    main_actors: List[str]
    average_rating: float
    popularity_score: float
    genre_match_score: float
    actor_popularity_score: float
    preprocessed_rating: float


class DataPreprocessor:
    """
    Advanced data preprocessing system for movie recommendation.
    
    This class handles the complex task of transforming raw movie data
    and user preferences into the standardized inputs required by the
    fuzzy logic system. It provides sophisticated algorithms for:
    
    - Genre preference modeling and matching
    - Actor popularity calculation and scoring
    - User rating behavior analysis
    - Data quality validation and cleaning
    """
    
    def __init__(self, genre_matching_strategy: GenreMatchingStrategy = GenreMatchingStrategy.WEIGHTED_OVERLAP,
                 actor_popularity_source: ActorPopularitySource = ActorPopularitySource.COMBINED_SCORE):
        """
        Initialize the data preprocessor.
        
        Args:
            genre_matching_strategy (GenreMatchingStrategy): Strategy for genre matching
            actor_popularity_source (ActorPopularitySource): Source for actor popularity scores
        """
        self.genre_matching_strategy = genre_matching_strategy
        self.actor_popularity_source = actor_popularity_source
        
        # Initialize data stores
        self.movie_database = pd.DataFrame()
        self.user_profiles = {}
        self.genre_hierarchy = self._build_genre_hierarchy()
        self.actor_popularity_cache = {}
        
        # Statistics and validation
        self.processing_stats = {
            'movies_processed': 0,
            'users_profiled': 0,
            'genres_identified': 0,
            'actors_cataloged': 0
        }
        
        print(f"Data Preprocessor initialized with:")
        print(f"  - Genre matching: {genre_matching_strategy.value}")
        print(f"  - Actor popularity: {actor_popularity_source.value}")
    
    def load_movie_data(self, data_source: Union[str, pd.DataFrame], 
                       column_mapping: Optional[Dict[str, str]] = None) -> None:
        """
        Load and validate movie data from various sources.
        
        Args:
            data_source (Union[str, pd.DataFrame]): Path to CSV file or DataFrame
            column_mapping (Dict[str, str]): Mapping of column names to standard format
        """
        
        # Load data
        if isinstance(data_source, str):
            try:
                self.movie_database = pd.read_csv(data_source)
                print(f"Loaded movie data from: {data_source}")
            except Exception as e:
                print(f"Error loading movie data: {e}")
                # Create sample data if file doesn't exist
                self.movie_database = self._create_sample_movie_data()
                print("Created sample movie database for demonstration")
        else:
            self.movie_database = data_source.copy()
        
        # Apply column mapping if provided
        if column_mapping:
            self.movie_database = self.movie_database.rename(columns=column_mapping)
        
        # Standardize column names
        self._standardize_columns()
        
        # Validate and clean data
        self._validate_movie_data()
        
        # Update statistics
        self.processing_stats['movies_processed'] = len(self.movie_database)
        self.processing_stats['genres_identified'] = len(self._extract_all_genres())
        self.processing_stats['actors_cataloged'] = len(self._extract_all_actors())
        
        print(f"Movie database loaded: {len(self.movie_database)} movies")
    
    def create_user_profile(self, user_id: str, rating_history: List[Tuple[str, float]], 
                          explicit_preferences: Optional[Dict[str, Any]] = None) -> UserProfile:
        """
        Create a comprehensive user profile from rating history and preferences.
        
        Args:
            user_id (str): Unique user identifier
            rating_history (List[Tuple[str, float]]): List of (movie_id, rating) pairs
            explicit_preferences (Dict[str, Any]): Explicit user preferences (optional)
        
        Returns:
            UserProfile: Comprehensive user preference profile
        """
        
        # Extract ratings
        ratings = [rating for _, rating in rating_history]
        movie_ids = [movie_id for movie_id, _ in rating_history]
        
        # Analyze rating behavior
        rating_behavior = self._analyze_rating_behavior(ratings)
        
        # Infer genre preferences from rating history
        preferred_genres = self._infer_genre_preferences(movie_ids, ratings)
        
        # Infer actor preferences from rating history
        preferred_actors = self._infer_actor_preferences(movie_ids, ratings)
        
        # Incorporate explicit preferences if provided
        if explicit_preferences:
            if 'genres' in explicit_preferences:
                preferred_genres.update(explicit_preferences['genres'])
            if 'actors' in explicit_preferences:
                preferred_actors.update(explicit_preferences['actors'])
        
        # Create user profile
        profile = UserProfile(
            user_id=user_id,
            rating_history=ratings,
            preferred_genres=preferred_genres,
            preferred_actors=preferred_actors,
            rating_behavior=rating_behavior,
            last_updated=pd.Timestamp.now().isoformat()
        )
        
        # Store profile
        self.user_profiles[user_id] = profile
        self.processing_stats['users_profiled'] = len(self.user_profiles)
        
        print(f"Created user profile for {user_id}")
        print(f"  - Rating history: {len(ratings)} movies")
        print(f"  - Preferred genres: {len(preferred_genres)}")
        print(f"  - Preferred actors: {len(preferred_actors)}")
        
        return profile
    
    def preprocess_movie_for_recommendation(self, movie_id: str, user_id: str) -> MovieFeatures:
        """
        Preprocess a specific movie for recommendation to a specific user.
        
        Args:
            movie_id (str): Movie identifier
            user_id (str): User identifier
        
        Returns:
            MovieFeatures: Preprocessed movie features ready for fuzzy logic
        """
        
        # Get movie data
        movie_data = self._get_movie_data(movie_id)
        if movie_data.empty:
            raise ValueError(f"Movie {movie_id} not found in database")
        
        # Get user profile
        if user_id not in self.user_profiles:
            raise ValueError(f"User profile {user_id} not found")
        
        user_profile = self.user_profiles[user_id]
        
        # Extract movie information
        title = movie_data['title'].iloc[0]
        genres = self._parse_genres(movie_data['genres'].iloc[0])
        actors = self._parse_actors(movie_data['actors'].iloc[0])
        avg_rating = float(movie_data['average_rating'].iloc[0])
        
        # Calculate fuzzy logic inputs
        
        # 1. User Rating Input (based on user's rating behavior and movie quality)
        preprocessed_rating = self._calculate_user_rating_input(avg_rating, user_profile)
        
        # 2. Actor Popularity Score
        actor_popularity_score = self._calculate_actor_popularity(actors)
        
        # 3. Genre Match Score
        genre_match_score = self._calculate_genre_match(genres, user_profile.preferred_genres)
        
        # 4. Overall popularity score
        popularity_score = self._calculate_movie_popularity(movie_data)
        
        # Create MovieFeatures object
        features = MovieFeatures(
            movie_id=movie_id,
            title=title,
            genres=genres,
            main_actors=actors,
            average_rating=avg_rating,
            popularity_score=popularity_score,
            genre_match_score=genre_match_score,
            actor_popularity_score=actor_popularity_score,
            preprocessed_rating=preprocessed_rating
        )
        
        return features
    
    def batch_preprocess_movies(self, movie_ids: List[str], user_id: str) -> List[MovieFeatures]:
        """
        Preprocess multiple movies for recommendation in batch.
        
        Args:
            movie_ids (List[str]): List of movie identifiers
            user_id (str): User identifier
        
        Returns:
            List[MovieFeatures]: List of preprocessed movie features
        """
        
        results = []
        
        for movie_id in movie_ids:
            try:
                features = self.preprocess_movie_for_recommendation(movie_id, user_id)
                results.append(features)
            except Exception as e:
                print(f"Error preprocessing movie {movie_id}: {e}")
                continue
        
        print(f"Batch processed {len(results)}/{len(movie_ids)} movies for user {user_id}")
        
        return results
    
    def _create_sample_movie_data(self) -> pd.DataFrame:
        """Create sample movie data for demonstration purposes."""
        
        sample_data = {
            'movie_id': [f'movie_{i:03d}' for i in range(1, 51)],
            'title': [
                'The Dark Knight', 'Inception', 'Pulp Fiction', 'The Shawshank Redemption',
                'Forrest Gump', 'The Matrix', 'Goodfellas', 'The Godfather',
                'Fight Club', 'The Lord of the Rings', 'Star Wars', 'Titanic',
                'Avatar', 'The Avengers', 'Jurassic Park', 'Terminator 2',
                'Alien', 'Blade Runner', 'Casablanca', 'Gone with the Wind',
                'Citizen Kane', 'Vertigo', 'Psycho', 'North by Northwest',
                'Rear Window', 'Sunset Boulevard', 'Some Like It Hot', 'The Apartment',
                'On the Waterfront', 'Singin\' in the Rain', 'The Wizard of Oz',
                'Lawrence of Arabia', 'The Sound of Music', 'Schindler\'s List',
                'Raging Bull', 'Taxi Driver', 'The Deer Hunter', 'Apocalypse Now',
                'The Graduate', 'Bonnie and Clyde', 'Chinatown', 'The French Connection',
                'Unforgiven', 'Goodfellas', 'The Silence of the Lambs', 'Thelma & Louise',
                'Dances with Wolves', 'The Last of the Mohicans', 'Braveheart', 'Gladiator'
            ],
            'genres': [
                'Action|Crime|Drama', 'Action|Sci-Fi|Thriller', 'Crime|Drama', 'Drama',
                'Drama|Romance', 'Action|Sci-Fi', 'Crime|Drama', 'Crime|Drama',
                'Drama|Thriller', 'Adventure|Drama|Fantasy', 'Action|Adventure|Sci-Fi', 'Drama|Romance',
                'Action|Adventure|Sci-Fi', 'Action|Adventure|Sci-Fi', 'Adventure|Sci-Fi|Thriller', 'Action|Sci-Fi|Thriller',
                'Horror|Sci-Fi|Thriller', 'Sci-Fi|Thriller', 'Drama|Romance', 'Drama|Romance',
                'Drama', 'Mystery|Romance|Thriller', 'Horror|Mystery|Thriller', 'Mystery|Thriller',
                'Mystery|Thriller', 'Drama|Film-Noir', 'Comedy|Romance', 'Comedy|Drama|Romance',
                'Crime|Drama', 'Comedy|Musical|Romance', 'Adventure|Family|Fantasy|Musical',
                'Adventure|Biography|Drama|History', 'Biography|Drama|Family|Musical', 'Biography|Drama|History',
                'Biography|Drama|Sport', 'Crime|Drama', 'Drama|War', 'Drama|War',
                'Comedy|Drama|Romance', 'Action|Biography|Crime|Drama', 'Drama|Mystery|Thriller', 'Action|Crime|Thriller',
                'Drama|Western', 'Crime|Drama', 'Crime|Horror|Thriller', 'Adventure|Crime|Drama',
                'Adventure|Drama|Western', 'Action|Drama|Romance|War', 'Biography|Drama|History|War', 'Action|Adventure|Drama'
            ],
            'actors': [
                'Christian Bale|Heath Ledger|Aaron Eckhart', 'Leonardo DiCaprio|Marion Cotillard|Tom Hardy',
                'John Travolta|Samuel L. Jackson|Uma Thurman', 'Tim Robbins|Morgan Freeman',
                'Tom Hanks|Robin Wright|Gary Sinise', 'Keanu Reeves|Laurence Fishburne|Carrie-Anne Moss',
                'Robert De Niro|Ray Liotta|Joe Pesci', 'Marlon Brando|Al Pacino|James Caan',
                'Brad Pitt|Edward Norton|Helena Bonham Carter', 'Elijah Wood|Ian McKellen|Orlando Bloom',
                'Mark Hamill|Harrison Ford|Carrie Fisher', 'Leonardo DiCaprio|Kate Winslet|Billy Zane',
                'Sam Worthington|Zoe Saldana|Sigourney Weaver', 'Robert Downey Jr.|Chris Evans|Mark Ruffalo',
                'Sam Neill|Laura Dern|Jeff Goldblum', 'Arnold Schwarzenegger|Linda Hamilton|Edward Furlong',
                'Sigourney Weaver|Tom Skerritt|John Hurt', 'Harrison Ford|Rutger Hauer|Sean Young',
                'Humphrey Bogart|Ingrid Bergman|Paul Henreid', 'Clark Gable|Vivien Leigh|Thomas Mitchell',
                'Orson Welles|Joseph Cotten|Dorothy Comingore', 'James Stewart|Kim Novak|Barbara Bel Geddes',
                'Anthony Perkins|Janet Leigh|Vera Miles', 'Cary Grant|Eva Marie Saint|James Mason',
                'James Stewart|Grace Kelly|Wendell Corey', 'William Holden|Gloria Swanson|Erich von Stroheim',
                'Tony Curtis|Jack Lemmon|Marilyn Monroe', 'Jack Lemmon|Shirley MacLaine|Fred MacMurray',
                'Marlon Brando|Karl Malden|Lee J. Cobb', 'Gene Kelly|Donald O\'Connor|Debbie Reynolds',
                'Judy Garland|Frank Morgan|Ray Bolger', 'Peter O\'Toole|Alec Guinness|Anthony Quinn',
                'Julie Andrews|Christopher Plummer|Eleanor Parker', 'Liam Neeson|Ben Kingsley|Ralph Fiennes',
                'Robert De Niro|Cathy Moriarty|Joe Pesci', 'Robert De Niro|Jodie Foster|Cybill Shepherd',
                'Robert De Niro|Christopher Walken|John Cazale', 'Marlon Brando|Robert Duvall|Martin Sheen',
                'Anne Bancroft|Dustin Hoffman|Katharine Ross', 'Warren Beatty|Faye Dunaway|Michael J. Pollard',
                'Jack Nicholson|Faye Dunaway|John Huston', 'Gene Hackman|Roy Scheider|Fernando Rey',
                'Clint Eastwood|Gene Hackman|Morgan Freeman', 'Robert De Niro|Ray Liotta|Joe Pesci',
                'Jodie Foster|Anthony Hopkins|Scott Glenn', 'Susan Sarandon|Geena Davis|Harvey Keitel',
                'Kevin Costner|Mary McDonnell|Graham Greene', 'Daniel Day-Lewis|Madeleine Stowe|Russell Means',
                'Mel Gibson|Sophie Marceau|Patrick McGoohan', 'Russell Crowe|Joaquin Phoenix|Connie Nielsen'
            ],
            'average_rating': np.random.uniform(6.5, 9.5, 50).round(1),
            'release_year': np.random.randint(1990, 2024, 50),
            'runtime': np.random.randint(90, 180, 50)
        }
        
        return pd.DataFrame(sample_data)
    
    def _standardize_columns(self) -> None:
        """Standardize column names to expected format."""
        
        expected_columns = ['movie_id', 'title', 'genres', 'actors', 'average_rating']
        current_columns = self.movie_database.columns.tolist()
        
        # Common column name mappings
        column_mappings = {
            'id': 'movie_id',
            'name': 'title',
            'genre': 'genres',
            'cast': 'actors',
            'actor': 'actors',
            'rating': 'average_rating',
            'imdb_rating': 'average_rating',
            'score': 'average_rating'
        }
        
        # Apply automatic mappings
        for old_name, new_name in column_mappings.items():
            if old_name in current_columns and new_name not in current_columns:
                self.movie_database = self.movie_database.rename(columns={old_name: new_name})
        
        # Ensure required columns exist (create dummy columns if missing)
        for col in expected_columns:
            if col not in self.movie_database.columns:
                if col == 'movie_id':
                    self.movie_database[col] = [f'movie_{i}' for i in range(len(self.movie_database))]
                elif col == 'title':
                    self.movie_database[col] = f'Unknown Title'
                elif col == 'genres':
                    self.movie_database[col] = 'Unknown'
                elif col == 'actors':
                    self.movie_database[col] = 'Unknown Actor'
                elif col == 'average_rating':
                    self.movie_database[col] = 5.0
    
    def _validate_movie_data(self) -> None:
        """Validate and clean movie data."""
        
        initial_count = len(self.movie_database)
        
        # Remove duplicates
        self.movie_database = self.movie_database.drop_duplicates(subset=['movie_id'], keep='first')
        
        # Clean ratings (ensure numeric and within valid range)
        self.movie_database['average_rating'] = pd.to_numeric(
            self.movie_database['average_rating'], errors='coerce'
        )
        self.movie_database = self.movie_database.dropna(subset=['average_rating'])
        self.movie_database['average_rating'] = self.movie_database['average_rating'].clip(1.0, 10.0)
        
        # Clean genres and actors (remove null values)
        self.movie_database = self.movie_database.dropna(subset=['genres', 'actors'])
        
        # Clean string columns
        string_columns = ['title', 'genres', 'actors']
        for col in string_columns:
            if col in self.movie_database.columns:
                self.movie_database[col] = self.movie_database[col].astype(str).str.strip()
        
        final_count = len(self.movie_database)
        
        if final_count < initial_count:
            print(f"Data cleaning: {initial_count - final_count} invalid records removed")
    
    def _build_genre_hierarchy(self) -> Dict[str, List[str]]:
        """Build a hierarchical genre classification system."""
        
        return {
            'Action': ['Action', 'Adventure', 'Thriller', 'War'],
            'Drama': ['Drama', 'Biography', 'History', 'Romance'],
            'Comedy': ['Comedy', 'Family', 'Animation'],
            'Sci-Fi': ['Sci-Fi', 'Fantasy', 'Horror'],
            'Crime': ['Crime', 'Mystery', 'Film-Noir'],
            'Musical': ['Musical', 'Music'],
            'Documentary': ['Documentary'],
            'Western': ['Western'],
            'Sport': ['Sport']
        }
    
    def _get_movie_data(self, movie_id: str) -> pd.DataFrame:
        """Get movie data by ID."""
        return self.movie_database[self.movie_database['movie_id'] == movie_id]
    
    def _parse_genres(self, genre_string: str) -> List[str]:
        """Parse genre string into list of genres."""
        if pd.isna(genre_string) or genre_string == 'Unknown':
            return ['Unknown']
        
        # Handle various separators
        separators = ['|', ',', ';', '/', '&']
        genres = [genre_string]
        
        for sep in separators:
            new_genres = []
            for genre in genres:
                new_genres.extend([g.strip() for g in genre.split(sep)])
            genres = new_genres
        
        # Clean and validate genres
        cleaned_genres = []
        for genre in genres:
            genre = re.sub(r'[^a-zA-Z\s-]', '', genre).strip()
            if genre and len(genre) > 1:
                cleaned_genres.append(genre.title())
        
        return cleaned_genres if cleaned_genres else ['Unknown']
    
    def _parse_actors(self, actor_string: str) -> List[str]:
        """Parse actor string into list of actors."""
        if pd.isna(actor_string) or actor_string == 'Unknown Actor':
            return ['Unknown Actor']
        
        # Handle various separators
        separators = ['|', ',', ';', '&', ' and ']
        actors = [actor_string]
        
        for sep in separators:
            new_actors = []
            for actor in actors:
                new_actors.extend([a.strip() for a in actor.split(sep)])
            actors = new_actors
        
        # Clean actor names
        cleaned_actors = []
        for actor in actors:
            # Remove non-alphabetic characters except spaces, hyphens, and apostrophes
            actor = re.sub(r'[^a-zA-Z\s\'-]', '', actor).strip()
            if actor and len(actor) > 2:
                # Capitalize properly (handle names like "O'Connor", "Van Der Berg")
                words = actor.split()
                capitalized_words = []
                for word in words:
                    if "'" in word:
                        parts = word.split("'")
                        capitalized_parts = [part.capitalize() for part in parts]
                        capitalized_words.append("'".join(capitalized_parts))
                    else:
                        capitalized_words.append(word.capitalize())
                cleaned_actors.append(' '.join(capitalized_words))
        
        return cleaned_actors[:5] if cleaned_actors else ['Unknown Actor']  # Limit to top 5 actors
    
    def _extract_all_genres(self) -> List[str]:
        """Extract all unique genres from the database."""
        all_genres = set()
        
        for genre_string in self.movie_database['genres']:
            genres = self._parse_genres(genre_string)
            all_genres.update(genres)
        
        return sorted(list(all_genres))
    
    def _extract_all_actors(self) -> List[str]:
        """Extract all unique actors from the database."""
        all_actors = set()
        
        for actor_string in self.movie_database['actors']:
            actors = self._parse_actors(actor_string)
            all_actors.update(actors)
        
        return sorted(list(all_actors))
    
    def _analyze_rating_behavior(self, ratings: List[float]) -> Dict[str, float]:
        """Analyze user rating behavior patterns."""
        
        if not ratings:
            return {'mean': 5.0, 'std': 1.0, 'skewness': 0.0, 'range': 0.0}
        
        ratings_array = np.array(ratings)
        
        return {
            'mean': float(np.mean(ratings_array)),
            'std': float(np.std(ratings_array)),
            'skewness': float(self._calculate_skewness(ratings_array)),
            'range': float(np.max(ratings_array) - np.min(ratings_array)),
            'harsh_critic': float(np.mean(ratings_array) < 6.0),
            'generous_rater': float(np.mean(ratings_array) > 8.0)
        }
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Calculate skewness of data."""
        if len(data) < 3:
            return 0.0
        
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0
        
        n = len(data)
        skewness = (n / ((n - 1) * (n - 2))) * np.sum(((data - mean) / std) ** 3)
        
        return skewness
    
    def _infer_genre_preferences(self, movie_ids: List[str], ratings: List[float]) -> Dict[str, float]:
        """Infer genre preferences from rating history."""
        
        genre_ratings = defaultdict(list)
        
        # Collect ratings by genre
        for movie_id, rating in zip(movie_ids, ratings):
            movie_data = self._get_movie_data(movie_id)
            if not movie_data.empty:
                genres = self._parse_genres(movie_data['genres'].iloc[0])
                for genre in genres:
                    genre_ratings[genre].append(rating)
        
        # Calculate preference scores
        genre_preferences = {}
        
        for genre, genre_rating_list in genre_ratings.items():
            if genre_rating_list:
                avg_rating = np.mean(genre_rating_list)
                # Convert to 0-100 scale with boost for high ratings
                preference_score = ((avg_rating - 1) / 9) * 100
                # Boost score for consistently high ratings
                if avg_rating > 7.0 and len(genre_rating_list) >= 3:
                    preference_score = min(100, preference_score * 1.2)
                
                genre_preferences[genre] = max(0, min(100, preference_score))
        
        return genre_preferences
    
    def _infer_actor_preferences(self, movie_ids: List[str], ratings: List[float]) -> Dict[str, float]:
        """Infer actor preferences from rating history."""
        
        actor_ratings = defaultdict(list)
        
        # Collect ratings by actor
        for movie_id, rating in zip(movie_ids, ratings):
            movie_data = self._get_movie_data(movie_id)
            if not movie_data.empty:
                actors = self._parse_actors(movie_data['actors'].iloc[0])
                for actor in actors:
                    actor_ratings[actor].append(rating)
        
        # Calculate preference scores
        actor_preferences = {}
        
        for actor, actor_rating_list in actor_ratings.items():
            if len(actor_rating_list) >= 2:  # Require at least 2 movies
                avg_rating = np.mean(actor_rating_list)
                # Convert to 0-100 scale
                preference_score = ((avg_rating - 1) / 9) * 100
                # Boost for consistent high ratings
                if avg_rating > 7.5 and len(actor_rating_list) >= 3:
                    preference_score = min(100, preference_score * 1.15)
                
                actor_preferences[actor] = max(0, min(100, preference_score))
        
        return actor_preferences
    
    def _calculate_user_rating_input(self, movie_avg_rating: float, user_profile: UserProfile) -> float:
        """Calculate the user rating input for fuzzy logic system."""
        
        # Base rating adjusted for user's rating behavior
        user_mean = user_profile.rating_behavior.get('mean', 5.0)
        user_std = user_profile.rating_behavior.get('std', 1.0)
        
        # Adjust movie rating based on user's rating patterns
        if user_profile.rating_behavior.get('harsh_critic', 0) > 0.5:
            # Harsh critics might rate lower than average
            adjusted_rating = movie_avg_rating * 0.9
        elif user_profile.rating_behavior.get('generous_rater', 0) > 0.5:
            # Generous raters might rate higher than average
            adjusted_rating = min(10.0, movie_avg_rating * 1.1)
        else:
            # Average users
            adjusted_rating = movie_avg_rating
        
        # Ensure within valid range
        return max(1.0, min(10.0, adjusted_rating))
    
    def _calculate_actor_popularity(self, actors: List[str]) -> float:
        """Calculate actor popularity score (0-100)."""
        
        if not actors or actors == ['Unknown Actor']:
            return 0.0
        
        actor_scores = []
        
        for actor in actors:
            if actor in self.actor_popularity_cache:
                score = self.actor_popularity_cache[actor]
            else:
                # Calculate popularity based on movie count and ratings
                actor_movies = self.movie_database[
                    self.movie_database['actors'].str.contains(re.escape(actor), na=False)
                ]
                
                if len(actor_movies) > 0:
                    # Base score on number of movies
                    movie_count_score = min(100, len(actor_movies) * 10)
                    
                    # Adjust by average rating of their movies
                    avg_rating = actor_movies['average_rating'].mean()
                    rating_multiplier = (avg_rating - 1) / 9  # 0-1 scale
                    
                    score = movie_count_score * (0.7 + 0.3 * rating_multiplier)
                else:
                    score = 5.0  # Unknown actor base score
                
                self.actor_popularity_cache[actor] = score
            
            actor_scores.append(score)
        
        # Return maximum actor popularity (star power effect)
        return max(actor_scores)
    
    def _calculate_genre_match(self, movie_genres: List[str], 
                             user_genre_preferences: Dict[str, float]) -> float:
        """Calculate genre matching score (0-100)."""
        
        if not movie_genres or not user_genre_preferences:
            return 50.0  # Default moderate match
        
        if self.genre_matching_strategy == GenreMatchingStrategy.EXACT_MATCH:
            return self._exact_genre_match(movie_genres, user_genre_preferences)
        elif self.genre_matching_strategy == GenreMatchingStrategy.WEIGHTED_OVERLAP:
            return self._weighted_genre_overlap(movie_genres, user_genre_preferences)
        else:
            # Default to weighted overlap
            return self._weighted_genre_overlap(movie_genres, user_genre_preferences)
    
    def _exact_genre_match(self, movie_genres: List[str], 
                          user_preferences: Dict[str, float]) -> float:
        """Calculate exact genre match score."""
        
        match_scores = []
        
        for genre in movie_genres:
            if genre in user_preferences:
                match_scores.append(user_preferences[genre])
            else:
                match_scores.append(5.0)  # Severe penalty for non-preferred genres (was 25.0)
        
        return max(match_scores) if match_scores else 5.0
    
    def _weighted_genre_overlap(self, movie_genres: List[str], 
                               user_preferences: Dict[str, float]) -> float:
        """Calculate weighted genre overlap score."""
        
        total_weight = 0
        weighted_score = 0
        
        for i, genre in enumerate(movie_genres):
            # Weight decreases for later genres (assume order indicates importance)
            weight = 1.0 / (i + 1)
            
            if genre in user_preferences:
                genre_score = user_preferences[genre]
            else:
                # Check hierarchical matching
                genre_score = self._hierarchical_genre_match(genre, user_preferences)
            
            weighted_score += weight * genre_score
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 25.0
    
    def _hierarchical_genre_match(self, movie_genre: str, 
                                 user_preferences: Dict[str, float]) -> float:
        """Match genres using hierarchical classification."""
        
        # Find parent category for the movie genre
        parent_category = None
        for category, genres in self.genre_hierarchy.items():
            if movie_genre in genres:
                parent_category = category
                break
        
        if parent_category:
            # Look for preferences in the same category
            category_scores = []
            for pref_genre, score in user_preferences.items():
                if pref_genre in self.genre_hierarchy.get(parent_category, []):
                    category_scores.append(score)
            
            if category_scores:
                return np.mean(category_scores) * 0.7  # Reduced score for indirect match
        
        return 25.0  # Default score for no match
    
    def _calculate_movie_popularity(self, movie_data: pd.DataFrame) -> float:
        """Calculate overall movie popularity score."""
        
        # Base popularity on rating
        rating = movie_data['average_rating'].iloc[0]
        popularity = ((rating - 1) / 9) * 100
        
        # Boost for additional factors if available
        if 'release_year' in movie_data.columns:
            year = movie_data['release_year'].iloc[0]
            current_year = pd.Timestamp.now().year
            
            # Recent movies get slight boost
            if current_year - year < 5:
                popularity *= 1.1
            # Classic movies (>30 years) also get boost
            elif current_year - year > 30:
                popularity *= 1.05
        
        return max(0, min(100, popularity))
    
    def get_preprocessing_stats(self) -> Dict[str, Any]:
        """Get comprehensive preprocessing statistics."""
        
        return {
            'processing_stats': self.processing_stats.copy(),
            'configuration': {
                'genre_matching_strategy': self.genre_matching_strategy.value,
                'actor_popularity_source': self.actor_popularity_source.value
            },
            'data_quality': {
                'movies_in_database': len(self.movie_database),
                'user_profiles_created': len(self.user_profiles),
                'genres_in_system': len(self._extract_all_genres()),
                'actors_in_system': len(self._extract_all_actors()),
                'actor_popularity_cache_size': len(self.actor_popularity_cache)
            }
        }
    
    def print_preprocessing_summary(self) -> None:
        """Print comprehensive preprocessing summary."""
        
        stats = self.get_preprocessing_stats()
        
        print("="*80)
        print("DATA PREPROCESSING SUMMARY")
        print("="*80)
        
        print(f"\nConfiguration:")
        print(f"  • Genre Matching Strategy: {stats['configuration']['genre_matching_strategy']}")
        print(f"  • Actor Popularity Source: {stats['configuration']['actor_popularity_source']}")
        
        print(f"\nData Processing Statistics:")
        for key, value in stats['processing_stats'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nData Quality Metrics:")
        for key, value in stats['data_quality'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        if self.user_profiles:
            print(f"\nUser Profile Analysis:")
            total_ratings = sum(len(profile.rating_history) for profile in self.user_profiles.values())
            avg_ratings_per_user = total_ratings / len(self.user_profiles) if self.user_profiles else 0
            print(f"  • Total Ratings Processed: {total_ratings}")
            print(f"  • Average Ratings per User: {avg_ratings_per_user:.1f}")
        
        print("="*80)


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the data preprocessing system.
    """
    
    print("Data Preprocessing System for Fuzzy Movie Recommendation")
    print("=" * 60)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor(
        genre_matching_strategy=GenreMatchingStrategy.WEIGHTED_OVERLAP,
        actor_popularity_source=ActorPopularitySource.COMBINED_SCORE
    )
    
    # Load sample movie data
    preprocessor.load_movie_data("sample_movies.csv")
    
    # Create sample user profile
    sample_rating_history = [
        ('movie_001', 8.5), ('movie_002', 9.0), ('movie_003', 7.5),
        ('movie_004', 9.5), ('movie_005', 8.0), ('movie_006', 8.5),
        ('movie_007', 7.0), ('movie_008', 9.0), ('movie_009', 8.5),
        ('movie_010', 7.5)
    ]
    
    user_profile = preprocessor.create_user_profile(
        user_id="user_001",
        rating_history=sample_rating_history
    )
    
    # Test movie preprocessing
    print(f"\nTesting Movie Preprocessing:")
    print("-" * 40)
    
    try:
        movie_features = preprocessor.preprocess_movie_for_recommendation("movie_001", "user_001")
        
        print(f"Movie: {movie_features.title}")
        print(f"Genres: {', '.join(movie_features.genres)}")
        print(f"Main Actors: {', '.join(movie_features.main_actors)}")
        print(f"Preprocessed Rating: {movie_features.preprocessed_rating:.2f}")
        print(f"Actor Popularity Score: {movie_features.actor_popularity_score:.2f}")
        print(f"Genre Match Score: {movie_features.genre_match_score:.2f}")
        
    except Exception as e:
        print(f"Error in preprocessing: {e}")
    
    # Print summary
    preprocessor.print_preprocessing_summary()
    
    # Test batch preprocessing
    print(f"\nTesting Batch Preprocessing:")
    print("-" * 40)
    
    batch_results = preprocessor.batch_preprocess_movies(
        ["movie_001", "movie_002", "movie_003"], "user_001"
    )
    
    for features in batch_results:
        print(f"{features.title}: Rating={features.preprocessed_rating:.1f}, "
              f"Actors={features.actor_popularity_score:.1f}, "
              f"Genre={features.genre_match_score:.1f}")
