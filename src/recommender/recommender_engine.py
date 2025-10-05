"""
Movie Recommendation Engine - Main Integration Module

This module serves as the primary interface for the fuzzy logic movie recommendation
system. It integrates all components:

- Data preprocessing and user profiling
- Fuzzy logic inference system
- Movie database management
- Recommendation ranking and filtering
- Explanation generation and user feedback

The RecommendationEngine class provides a complete, production-ready movie
recommendation system that uses fuzzy logic as its core decision-making mechanism.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from datetime import datetime
import warnings

# Import our custom modules
from fuzzy_logic.fuzzy_model import FuzzyMovieRecommender, RecommendationResult, DefuzzificationMethod
from fuzzy_logic.variables import FuzzyVariables
from fuzzy_logic.rules import FuzzyRuleEngine
from recommender.preprocessor import DataPreprocessor, UserProfile, MovieFeatures, GenreMatchingStrategy, ActorPopularitySource

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecommendationMode(Enum):
    """Enumeration of recommendation modes."""
    PERSONALIZED = "personalized"
    POPULAR = "popular"
    SIMILAR = "similar"
    EXPLORATORY = "exploratory"
    HYBRID = "hybrid"


class SortingCriteria(Enum):
    """Enumeration of sorting criteria for recommendations."""
    RECOMMENDATION_SCORE = "recommendation_score"
    CONFIDENCE_LEVEL = "confidence_level"
    MOVIE_RATING = "movie_rating"
    POPULARITY = "popularity"
    RELEASE_DATE = "release_date"
    COMBINED = "combined"


@dataclass
class RecommendationItem:
    """
    Complete recommendation item with all relevant information.
    
    Attributes:
        movie_features (MovieFeatures): Processed movie features
        fuzzy_result (RecommendationResult): Fuzzy logic recommendation result
        rank (int): Recommendation rank (1-based)
        recommendation_reason (str): Main reason for recommendation
        alternative_reasons (List[str]): Alternative recommendation reasons
        confidence_factors (Dict[str, float]): Detailed confidence breakdown
    """
    movie_features: MovieFeatures
    fuzzy_result: RecommendationResult
    rank: int
    recommendation_reason: str
    alternative_reasons: List[str] = field(default_factory=list)
    confidence_factors: Dict[str, float] = field(default_factory=dict)


@dataclass
class RecommendationSession:
    """
    Complete recommendation session information.
    
    Attributes:
        user_id (str): User identifier
        session_id (str): Unique session identifier
        recommendations (List[RecommendationItem]): List of recommendations
        session_config (Dict[str, Any]): Session configuration
        timestamp (str): Session timestamp
        performance_metrics (Dict[str, float]): Performance metrics
    """
    user_id: str
    session_id: str
    recommendations: List[RecommendationItem]
    session_config: Dict[str, Any]
    timestamp: str
    performance_metrics: Dict[str, float] = field(default_factory=dict)


class MovieRecommendationEngine:
    """
    Complete fuzzy logic-based movie recommendation engine.
    
    This class orchestrates the entire recommendation process, from data loading
    and user profiling to fuzzy logic inference and result presentation. It
    provides multiple recommendation modes and comprehensive explanation capabilities.
    
    Key Features:
    - Fuzzy logic-based decision making
    - Personalized user profiling
    - Multiple recommendation strategies
    - Detailed explanations and confidence metrics
    - Batch processing capabilities
    - Performance monitoring and optimization
    """
    
    def __init__(self, 
                 defuzzification_method: DefuzzificationMethod = DefuzzificationMethod.CENTROID,
                 genre_matching_strategy: GenreMatchingStrategy = GenreMatchingStrategy.WEIGHTED_OVERLAP,
                 actor_popularity_source: ActorPopularitySource = ActorPopularitySource.COMBINED_SCORE):
        """
        Initialize the movie recommendation engine.
        
        Args:
            defuzzification_method (DefuzzificationMethod): Fuzzy logic defuzzification method
            genre_matching_strategy (GenreMatchingStrategy): Genre matching strategy
            actor_popularity_source (ActorPopularitySource): Actor popularity calculation method
        """
        
        # Initialize core components
        self.fuzzy_recommender = FuzzyMovieRecommender(defuzzification_method)
        self.data_preprocessor = DataPreprocessor(genre_matching_strategy, actor_popularity_source)
        
        # Configuration
        self.config = {
            'defuzzification_method': defuzzification_method.value if hasattr(defuzzification_method, 'value') else str(defuzzification_method),
            'genre_matching_strategy': genre_matching_strategy.value if hasattr(genre_matching_strategy, 'value') else str(genre_matching_strategy),
            'actor_popularity_source': actor_popularity_source.value if hasattr(actor_popularity_source, 'value') else str(actor_popularity_source),
            'min_recommendation_score': 25.0,
            'max_recommendations': 50,
            'confidence_threshold': 0.3
        }
        
        # State management
        self.is_initialized = False
        self.recommendation_sessions = {}
        self.system_statistics = {
            'total_recommendations': 0,
            'successful_sessions': 0,
            'average_processing_time': 0.0,
            'user_satisfaction_scores': []
        }
        
        logger.info("Movie Recommendation Engine initialized")
        logger.info(f"Configuration: {self.config}")
    
    def initialize_system(self, movie_data_source: Union[str, pd.DataFrame],
                         column_mapping: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize the recommendation system with movie data.
        
        Args:
            movie_data_source (Union[str, pd.DataFrame]): Movie data source
            column_mapping (Dict[str, str]): Column name mapping (optional)
        """
        
        try:
            # Load movie data
            self.data_preprocessor.load_movie_data(movie_data_source, column_mapping)
            
            # Validate system components
            self._validate_system_components()
            
            self.is_initialized = True
            logger.info("Recommendation system successfully initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize system: {e}")
            raise
    
    def create_user_profile(self, user_id: str, rating_history: List[Tuple[str, float]],
                          explicit_preferences: Optional[Dict[str, Any]] = None) -> UserProfile:
        """
        Create or update a user profile.
        
        Args:
            user_id (str): Unique user identifier
            rating_history (List[Tuple[str, float]]): User's rating history
            explicit_preferences (Dict[str, Any]): Explicit user preferences
        
        Returns:
            UserProfile: Created or updated user profile
        """
        
        if not self.is_initialized:
            raise RuntimeError("System must be initialized before creating user profiles")
        
        try:
            profile = self.data_preprocessor.create_user_profile(
                user_id, rating_history, explicit_preferences
            )
            
            logger.info(f"User profile created/updated for {user_id}")
            return profile
            
        except Exception as e:
            logger.error(f"Error creating user profile for {user_id}: {e}")
            raise
    
    def generate_recommendations(self, user_id: str, 
                               mode: RecommendationMode = RecommendationMode.PERSONALIZED,
                               num_recommendations: int = 10,
                               movie_candidates: Optional[List[str]] = None,
                               exclude_movies: Optional[List[str]] = None,
                               min_score: Optional[float] = None,
                               sorting_criteria: SortingCriteria = SortingCriteria.COMBINED) -> RecommendationSession:
        """
        Generate movie recommendations for a user.
        
        Args:
            user_id (str): User identifier
            mode (RecommendationMode): Recommendation mode
            num_recommendations (int): Number of recommendations to generate
            movie_candidates (List[str]): Specific movies to consider (optional)
            exclude_movies (List[str]): Movies to exclude (optional)
            min_score (float): Minimum recommendation score threshold (optional)
            sorting_criteria (SortingCriteria): Criteria for sorting recommendations
        
        Returns:
            RecommendationSession: Complete recommendation session
        """
        
        start_time = datetime.now()
        
        if not self.is_initialized:
            raise RuntimeError("System must be initialized before generating recommendations")
        
        if user_id not in self.data_preprocessor.user_profiles:
            raise ValueError(f"User profile for {user_id} not found. Create profile first.")
        
        try:
            # Generate session ID
            session_id = f"{user_id}_{start_time.strftime('%Y%m%d_%H%M%S')}"
            
            # Determine candidate movies
            candidates = self._get_candidate_movies(movie_candidates, exclude_movies or [])
            
            # Process movies and generate fuzzy recommendations
            recommendations = self._process_movie_candidates(user_id, candidates)
            
            # Filter and sort recommendations
            filtered_recommendations = self._filter_recommendations(
                recommendations, min_score or self.config['min_recommendation_score']
            )
            
            sorted_recommendations = self._sort_recommendations(
                filtered_recommendations, sorting_criteria
            )
            
            # Limit to requested number
            final_recommendations = sorted_recommendations[:num_recommendations]
            
            # Add ranking and enhanced explanations
            recommendation_items = self._create_recommendation_items(final_recommendations)
            
            # Calculate performance metrics
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            performance_metrics = {
                'processing_time_seconds': processing_time,
                'candidates_processed': len(candidates),
                'recommendations_generated': len(recommendation_items),
                'average_confidence': np.mean([item.fuzzy_result.confidence_level for item in recommendation_items]) if recommendation_items else 0.0,
                'average_score': np.mean([item.fuzzy_result.recommendation_score for item in recommendation_items]) if recommendation_items else 0.0
            }
            
            # Create session object
            session = RecommendationSession(
                user_id=user_id,
                session_id=session_id,
                recommendations=recommendation_items,
                session_config={
                    'mode': mode.value,
                    'num_requested': num_recommendations,
                    'sorting_criteria': sorting_criteria.value,
                    'min_score': min_score or self.config['min_recommendation_score']
                },
                timestamp=start_time.isoformat(),
                performance_metrics=performance_metrics
            )
            
            # Store session
            self.recommendation_sessions[session_id] = session
            
            # Update system statistics
            self._update_system_statistics(session)
            
            logger.info(f"Generated {len(recommendation_items)} recommendations for {user_id} in {processing_time:.2f}s")
            
            return session
            
        except Exception as e:
            logger.error(f"Error generating recommendations for {user_id}: {e}")
            raise
    
    def get_recommendation_explanation(self, session_id: str, movie_rank: int) -> Dict[str, Any]:
        """
        Get detailed explanation for a specific recommendation.
        
        Args:
            session_id (str): Recommendation session ID
            movie_rank (int): Rank of the movie to explain (1-based)
        
        Returns:
            Dict[str, Any]: Detailed explanation
        """
        
        if session_id not in self.recommendation_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.recommendation_sessions[session_id]
        
        if not (1 <= movie_rank <= len(session.recommendations)):
            raise ValueError(f"Movie rank {movie_rank} is out of range")
        
        recommendation = session.recommendations[movie_rank - 1]
        
        # Generate comprehensive explanation
        explanation = {
            'movie_info': {
                'title': recommendation.movie_features.title,
                'genres': recommendation.movie_features.genres,
                'main_actors': recommendation.movie_features.main_actors,
                'average_rating': recommendation.movie_features.average_rating
            },
            'recommendation_metrics': {
                'score': recommendation.fuzzy_result.recommendation_score,
                'confidence': recommendation.fuzzy_result.confidence_level,
                'rank': recommendation.rank
            },
            'fuzzy_logic_inputs': {
                'user_rating_input': recommendation.movie_features.preprocessed_rating,
                'actor_popularity_score': recommendation.movie_features.actor_popularity_score,
                'genre_match_score': recommendation.movie_features.genre_match_score
            },
            'membership_degrees': recommendation.fuzzy_result.membership_degrees,
            'activated_rules': recommendation.fuzzy_result.activated_rules,
            'detailed_explanation': recommendation.fuzzy_result.explanation,
            'recommendation_reason': recommendation.recommendation_reason,
            'alternative_reasons': recommendation.alternative_reasons,
            'confidence_factors': recommendation.confidence_factors
        }
        
        return explanation
    
    def batch_recommend_for_users(self, user_requests: List[Dict[str, Any]]) -> Dict[str, RecommendationSession]:
        """
        Generate recommendations for multiple users in batch.
        
        Args:
            user_requests (List[Dict[str, Any]]): List of user recommendation requests
                Each request should contain: user_id and optional parameters
        
        Returns:
            Dict[str, RecommendationSession]: Recommendation sessions by user ID
        """
        
        results = {}
        
        for request in user_requests:
            try:
                user_id = request['user_id']
                mode = RecommendationMode(request.get('mode', 'personalized'))
                num_recommendations = request.get('num_recommendations', 10)
                
                session = self.generate_recommendations(
                    user_id=user_id,
                    mode=mode,
                    num_recommendations=num_recommendations
                )
                
                results[user_id] = session
                
            except Exception as e:
                logger.error(f"Error processing batch request for user {request.get('user_id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Batch processing completed: {len(results)}/{len(user_requests)} successful")
        
        return results
    
    def update_user_feedback(self, session_id: str, movie_rank: int, 
                           feedback_score: float, feedback_comments: Optional[str] = None) -> None:
        """
        Update user feedback for a recommendation.
        
        Args:
            session_id (str): Session identifier
            movie_rank (int): Movie rank in the recommendation list
            feedback_score (float): User feedback score (1-10)
            feedback_comments (str): Optional feedback comments
        """
        
        if session_id not in self.recommendation_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.recommendation_sessions[session_id]
        
        if not (1 <= movie_rank <= len(session.recommendations)):
            raise ValueError(f"Movie rank {movie_rank} is out of range")
        
        # Store feedback (in a real system, this would go to a database)
        recommendation = session.recommendations[movie_rank - 1]
        
        if not hasattr(recommendation, 'user_feedback'):
            recommendation.user_feedback = {}
        
        recommendation.user_feedback.update({
            'score': feedback_score,
            'comments': feedback_comments,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update system statistics
        self.system_statistics['user_satisfaction_scores'].append(feedback_score)
        
        logger.info(f"Feedback updated for session {session_id}, movie rank {movie_rank}: {feedback_score}/10")
    
    def _get_candidate_movies(self, movie_candidates: Optional[List[str]], 
                            exclude_movies: List[str]) -> List[str]:
        """Get list of candidate movies for recommendation."""
        
        if movie_candidates:
            candidates = movie_candidates
        else:
            # Use all movies in database
            candidates = self.data_preprocessor.movie_database['movie_id'].tolist()
        
        # Exclude specified movies
        candidates = [movie_id for movie_id in candidates if movie_id not in exclude_movies]
        
        return candidates
    
    def _process_movie_candidates(self, user_id: str, candidates: List[str]) -> List[Tuple[MovieFeatures, RecommendationResult]]:
        """Process movie candidates and generate fuzzy recommendations."""
        
        recommendations = []
        
        for movie_id in candidates:
            try:
                # Preprocess movie features
                movie_features = self.data_preprocessor.preprocess_movie_for_recommendation(movie_id, user_id)
                
                # Generate fuzzy recommendation
                fuzzy_result = self.fuzzy_recommender.recommend_movie(
                    user_rating=movie_features.preprocessed_rating,
                    actor_popularity=movie_features.actor_popularity_score,
                    genre_match=movie_features.genre_match_score,
                    include_explanation=True
                )
                
                recommendations.append((movie_features, fuzzy_result))
                
            except Exception as e:
                logger.warning(f"Error processing movie {movie_id}: {e}")
                continue
        
        return recommendations
    
    def _filter_recommendations(self, recommendations: List[Tuple[MovieFeatures, RecommendationResult]], 
                              min_score: float) -> List[Tuple[MovieFeatures, RecommendationResult]]:
        """Filter recommendations based on minimum score threshold."""
        
        return [
            (features, result) for features, result in recommendations
            if result.recommendation_score >= min_score
        ]
    
    def _sort_recommendations(self, recommendations: List[Tuple[MovieFeatures, RecommendationResult]], 
                            criteria: SortingCriteria) -> List[Tuple[MovieFeatures, RecommendationResult]]:
        """Sort recommendations based on specified criteria."""
        
        if criteria == SortingCriteria.RECOMMENDATION_SCORE:
            return sorted(recommendations, key=lambda x: x[1].recommendation_score, reverse=True)
        elif criteria == SortingCriteria.CONFIDENCE_LEVEL:
            return sorted(recommendations, key=lambda x: x[1].confidence_level, reverse=True)
        elif criteria == SortingCriteria.MOVIE_RATING:
            return sorted(recommendations, key=lambda x: x[0].average_rating, reverse=True)
        elif criteria == SortingCriteria.POPULARITY:
            return sorted(recommendations, key=lambda x: x[0].popularity_score, reverse=True)
        elif criteria == SortingCriteria.COMBINED:
            # Combined score: 60% recommendation score + 25% confidence + 15% movie rating
            def combined_score(item):
                features, result = item
                return (0.6 * result.recommendation_score + 
                       0.25 * result.confidence_level * 100 + 
                       0.15 * features.average_rating * 10)
            
            return sorted(recommendations, key=combined_score, reverse=True)
        else:
            # Default to recommendation score
            return sorted(recommendations, key=lambda x: x[1].recommendation_score, reverse=True)
    
    def _create_recommendation_items(self, recommendations: List[Tuple[MovieFeatures, RecommendationResult]]) -> List[RecommendationItem]:
        """Create enhanced recommendation items with explanations."""
        
        items = []
        
        for rank, (features, result) in enumerate(recommendations, 1):
            # Generate recommendation reason
            reason = self._generate_recommendation_reason(features, result)
            
            # Generate alternative reasons
            alt_reasons = self._generate_alternative_reasons(features, result)
            
            # Calculate confidence factors
            confidence_factors = self._calculate_confidence_factors(features, result)
            
            item = RecommendationItem(
                movie_features=features,
                fuzzy_result=result,
                rank=rank,
                recommendation_reason=reason,
                alternative_reasons=alt_reasons,
                confidence_factors=confidence_factors
            )
            
            items.append(item)
        
        return items
    
    def _generate_recommendation_reason(self, features: MovieFeatures, result: RecommendationResult) -> str:
        """Generate the primary recommendation reason."""
        
        # Determine strongest factors
        factors = {
            'genre_match': features.genre_match_score,
            'actor_popularity': features.actor_popularity_score,
            'movie_quality': features.preprocessed_rating * 10
        }
        
        strongest_factor = max(factors, key=factors.get)
        
        if strongest_factor == 'genre_match' and features.genre_match_score > 80:
            return f"Perfect genre match - this {', '.join(features.genres[:2])} movie aligns with your preferences"
        elif strongest_factor == 'actor_popularity' and features.actor_popularity_score > 80:
            return f"Features {features.main_actors[0]} and other popular actors you might enjoy"
        elif strongest_factor == 'movie_quality' and features.average_rating > 8.0:
            return f"Highly rated movie ({features.average_rating:.1f}/10) with excellent reviews"
        else:
            return f"Well-balanced recommendation combining quality, star power, and genre appeal"
    
    def _generate_alternative_reasons(self, features: MovieFeatures, result: RecommendationResult) -> List[str]:
        """Generate alternative recommendation reasons."""
        
        reasons = []
        
        if features.genre_match_score > 70:
            reasons.append(f"Strong genre alignment with your {', '.join(features.genres[:2])} preferences")
        
        if features.actor_popularity_score > 70:
            reasons.append(f"Features popular actors: {', '.join(features.main_actors[:2])}")
        
        if features.average_rating > 7.5:
            reasons.append(f"High-quality movie with {features.average_rating:.1f}/10 rating")
        
        if result.confidence_level > 0.8:
            reasons.append("High-confidence recommendation based on your viewing history")
        
        return reasons
    
    def _calculate_confidence_factors(self, features: MovieFeatures, result: RecommendationResult) -> Dict[str, float]:
        """Calculate detailed confidence factors."""
        
        return {
            'data_quality': min(1.0, (features.average_rating / 10) * 1.2),
            'preference_alignment': features.genre_match_score / 100,
            'star_power': features.actor_popularity_score / 100,
            'fuzzy_logic_confidence': result.confidence_level,
            'overall_certainty': (features.genre_match_score + features.actor_popularity_score + result.confidence_level * 100) / 300
        }
    
    def _validate_system_components(self) -> None:
        """Validate that all system components are properly initialized."""
        
        if not hasattr(self.fuzzy_recommender, 'variables'):
            raise RuntimeError("Fuzzy logic system not properly initialized")
        
        if len(self.data_preprocessor.movie_database) == 0:
            raise RuntimeError("No movie data loaded")
        
        # Test fuzzy logic system with sample input
        try:
            test_result = self.fuzzy_recommender.recommend_movie(7.0, 60.0, 75.0, include_explanation=False)
            if test_result.recommendation_score < 0 or test_result.recommendation_score > 100:
                raise RuntimeError("Fuzzy logic system producing invalid output")
        except Exception as e:
            raise RuntimeError(f"Fuzzy logic system validation failed: {e}")
    
    def _update_system_statistics(self, session: RecommendationSession) -> None:
        """Update system performance statistics."""
        
        self.system_statistics['total_recommendations'] += len(session.recommendations)
        self.system_statistics['successful_sessions'] += 1
        
        # Update average processing time
        current_avg = self.system_statistics['average_processing_time']
        current_count = self.system_statistics['successful_sessions']
        new_time = session.performance_metrics['processing_time_seconds']
        
        self.system_statistics['average_processing_time'] = (
            (current_avg * (current_count - 1) + new_time) / current_count
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status and statistics."""
        
        return {
            'system_info': {
                'is_initialized': self.is_initialized,
                'configuration': self.config,
                'movie_database_size': len(self.data_preprocessor.movie_database) if self.is_initialized else 0,
                'user_profiles_count': len(self.data_preprocessor.user_profiles),
                'active_sessions': len(self.recommendation_sessions)
            },
            'performance_stats': self.system_statistics.copy(),
            'fuzzy_system_info': self.fuzzy_recommender.get_system_info() if self.is_initialized else {},
            'preprocessing_stats': self.data_preprocessor.get_preprocessing_stats() if self.is_initialized else {}
        }
    
    def print_system_summary(self) -> None:
        """Print comprehensive system summary."""
        
        status = self.get_system_status()
        
        print("="*80)
        print("FUZZY LOGIC MOVIE RECOMMENDATION ENGINE - SYSTEM SUMMARY")
        print("="*80)
        
        print(f"\nSystem Status:")
        print(f"  • Initialized: {status['system_info']['is_initialized']}")
        print(f"  • Movies in Database: {status['system_info']['movie_database_size']}")
        print(f"  • User Profiles: {status['system_info']['user_profiles_count']}")
        print(f"  • Active Sessions: {status['system_info']['active_sessions']}")
        
        print(f"\nConfiguration:")
        for key, value in status['system_info']['configuration'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        if status['performance_stats']['successful_sessions'] > 0:
            print(f"\nPerformance Statistics:")
            print(f"  • Total Recommendations: {status['performance_stats']['total_recommendations']}")
            print(f"  • Successful Sessions: {status['performance_stats']['successful_sessions']}")
            print(f"  • Average Processing Time: {status['performance_stats']['average_processing_time']:.3f}s")
            
            if status['performance_stats']['user_satisfaction_scores']:
                avg_satisfaction = np.mean(status['performance_stats']['user_satisfaction_scores'])
                print(f"  • Average User Satisfaction: {avg_satisfaction:.2f}/10")
        
        print("="*80)
    
    # Additional methods for compatibility with main.py
    def load_data(self, movie_data: pd.DataFrame) -> None:
        """
        Load movie data into the system (convenience method for main.py compatibility).
        
        Args:
            movie_data (pd.DataFrame): Movie dataset to load
        """
        self.initialize_system(movie_data)
    
    def get_recommendations(self, user_preferences: Dict[str, Any], 
                          num_recommendations: int = 5) -> List[Tuple[Dict[str, Any], float, str]]:
        """
        Get movie recommendations based on user preferences (simplified interface for main.py).
        
        Args:
            user_preferences (Dict[str, Any]): User preferences dictionary
            num_recommendations (int): Number of recommendations to return
            
        Returns:
            List[Tuple[Dict[str, Any], float, str]]: List of (movie_dict, score, explanation) tuples
        """
        try:
            # Create a temporary user profile
            user_id = f"temp_user_{hash(str(user_preferences))}"
            
            # Create user profile from preferences
            rating_history = []  # Simplified for demo
            
            # Extract preferences
            preferred_genres = user_preferences.get('preferred_genres', [])
            favorite_actors = user_preferences.get('favorite_actors', [])
            min_rating = user_preferences.get('min_rating', 5.0)
            
            # Create explicit preferences dictionary
            explicit_preferences = {
                'preferred_genres': preferred_genres,
                'favorite_actors': favorite_actors,
                'min_rating_threshold': min_rating
            }
            
            # Create user profile
            self.create_user_profile(
                user_id=user_id,
                rating_history=rating_history,
                explicit_preferences=explicit_preferences
            )
            
            # Generate recommendations
            session = self.generate_recommendations(
                user_id=user_id,
                num_recommendations=num_recommendations,
                mode=RecommendationMode.PERSONALIZED
            )
            
            # Convert to expected format for main.py
            results = []
            for item in session.recommendations:
                # Access movie features from RecommendationItem
                movie_features = item.movie_features
                
                # Create movie dictionary
                movie_dict = {
                    'movie_id': movie_features.movie_id,
                    'title': movie_features.title,
                    'genres': '|'.join(movie_features.genres) if isinstance(movie_features.genres, list) else movie_features.genres,
                    'actors': ', '.join(movie_features.main_actors[:3]) if isinstance(movie_features.main_actors, list) else str(movie_features.main_actors),
                    'average_rating': movie_features.average_rating,
                    'release_year': getattr(movie_features, 'release_year', 2020)
                }
                
                # Get score and explanation from fuzzy result
                score = item.fuzzy_result.recommendation_score
                explanation = item.recommendation_reason
                
                results.append((movie_dict, score, explanation))
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            # Return empty results if error
            return []


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the complete movie recommendation engine.
    """
    
    print("Complete Fuzzy Logic Movie Recommendation Engine")
    print("=" * 50)
    
    # Initialize the recommendation engine
    engine = MovieRecommendationEngine(
        defuzzification_method=DefuzzificationMethod.CENTROID,
        genre_matching_strategy=GenreMatchingStrategy.WEIGHTED_OVERLAP,
        actor_popularity_source=ActorPopularitySource.COMBINED_SCORE
    )
    
    # Initialize system with sample data
    engine.initialize_system("sample_movies.csv")
    
    # Create sample user profile
    sample_rating_history = [
        ('movie_001', 8.5), ('movie_002', 9.0), ('movie_003', 7.5),
        ('movie_004', 9.5), ('movie_005', 8.0), ('movie_007', 7.0),
        ('movie_008', 9.0), ('movie_009', 8.5), ('movie_010', 7.5)
    ]
    
    user_profile = engine.create_user_profile(
        user_id="demo_user",
        rating_history=sample_rating_history,
        explicit_preferences={
            'genres': {'Action': 85, 'Drama': 75, 'Comedy': 60},
            'actors': {'Leonardo DiCaprio': 90, 'Christian Bale': 85}
        }
    )
    
    # Generate recommendations
    print(f"\nGenerating Recommendations for {user_profile.user_id}")
    print("-" * 50)
    
    session = engine.generate_recommendations(
        user_id="demo_user",
        mode=RecommendationMode.PERSONALIZED,
        num_recommendations=5,
        sorting_criteria=SortingCriteria.COMBINED
    )
    
    # Display recommendations
    print(f"\nTop {len(session.recommendations)} Recommendations:")
    print("-" * 50)
    
    for item in session.recommendations:
        print(f"\n{item.rank}. {item.movie_features.title}")
        print(f"   Genres: {', '.join(item.movie_features.genres)}")
        print(f"   Score: {item.fuzzy_result.recommendation_score:.1f}/100")
        print(f"   Confidence: {item.fuzzy_result.confidence_level:.2f}")
        print(f"   Reason: {item.recommendation_reason}")
    
    # Show detailed explanation for top recommendation
    if session.recommendations:
        print(f"\nDetailed Explanation for Top Recommendation:")
        print("-" * 50)
        
        explanation = engine.get_recommendation_explanation(session.session_id, 1)
        
        print(f"Movie: {explanation['movie_info']['title']}")
        print(f"Fuzzy Logic Inputs:")
        print(f"  • User Rating Input: {explanation['fuzzy_logic_inputs']['user_rating_input']:.2f}")
        print(f"  • Actor Popularity: {explanation['fuzzy_logic_inputs']['actor_popularity_score']:.2f}")
        print(f"  • Genre Match: {explanation['fuzzy_logic_inputs']['genre_match_score']:.2f}")
        print(f"Final Score: {explanation['recommendation_metrics']['score']:.1f}/100")
    
    # System summary
    print(f"\nSystem Performance Summary:")
    print("-" * 50)
    
    engine.print_system_summary()
    
    # Simulate user feedback
    if session.recommendations:
        engine.update_user_feedback(session.session_id, 1, 8.5, "Great recommendation!")
        print(f"\nUser feedback recorded for top recommendation")



