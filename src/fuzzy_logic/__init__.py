"""
Fuzzy Logic Components Package
Paquete de Componentes de Lógica Difusa

This package contains the core fuzzy logic implementation including:
- Fuzzy variables and membership functions
- Fuzzy rule engine with comprehensive rules
- Mamdani fuzzy inference system
- Advanced defuzzification methods

Este paquete contiene la implementación central de lógica difusa incluyendo:
- Variables difusas y funciones de membresía
- Motor de reglas difusas con reglas comprensivas
- Sistema de inferencia difusa Mamdani
- Métodos avanzados de defuzzificación
"""

# Import modules - using try/except for graceful fallback
try:
    from fuzzy_logic.variables import FuzzyVariables
    from fuzzy_logic.membership_func import MembershipFunctions
    from fuzzy_logic.rules import FuzzyRuleEngine
    from fuzzy_logic.fuzzy_model import FuzzyMovieRecommender
except ImportError:
    # Fallback for when modules are not properly importable
    pass

__all__ = [
    'FuzzyVariables',
    'MembershipFunctions', 
    'FuzzyRuleEngine',
    'FuzzyMovieRecommender'
]