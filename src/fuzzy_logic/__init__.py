"""
Fuzzy Logic Components Package

This package contains the core fuzzy logic implementation including:
- Fuzzy variables and membership functions
- Fuzzy rule engine with comprehensive rules
- Mamdani fuzzy inference system
- Advanced defuzzification methods
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