"""
Recommendation System Components Package

This package contains the recommendation engine and data processing components:
- Data preprocessing and user profiling
- Movie recommendation engine with fuzzy logic integration
- Performance monitoring and analysis
"""

# Import modules - using try/except for graceful fallback
try:
    from recommender.preprocessor import DataPreprocessor
    from recommender.recommender_engine import MovieRecommendationEngine
except ImportError:
    # Fallback for when modules are not properly importable
    pass

__all__ = [
    'DataPreprocessor',
    'MovieRecommendationEngine'
]