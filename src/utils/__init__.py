"""
Utilities Package
Paquete de Utilidades

This package contains utility functions and classes for:
- Data loading and management
- File format support
- Data quality assessment

Este paquete contiene funciones y clases de utilidad para:
- Carga y gestión de datos
- Soporte de formatos de archivo
- Evaluación de calidad de datos
"""

# Import modules - using try/except for graceful fallback
try:
    from utils.data_loader import EnhancedDataLoader
except ImportError:
    # Fallback for when modules are not properly importable
    pass

__all__ = [
    'EnhancedDataLoader'
]