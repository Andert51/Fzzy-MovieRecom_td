"""
Recommendation System Components Package
Paquete de Componentes del Sistema de Recomendación

This package contains the recommendation engine and data processing components:
- Data preprocessing and user profiling
- Movie recommendation engine with fuzzy logic integration
- Performance monitoring and analysis

Este paquete contiene el motor de recomendación y componentes de procesamiento de datos:
- Preprocesamiento de datos y perfilado de usuarios
- Motor de recomendación de películas con integración de lógica difusa
- Monitoreo y análisis de rendimiento
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