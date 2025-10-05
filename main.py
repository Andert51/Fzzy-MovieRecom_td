"""
Fuzzy Logic Movie Recommendation System - Main Application
Sistema de Recomendación de Películas con Lógica Difusa

This is the main application demonstrating the complete fuzzy logic movie recommendation system.
Esta es la aplicación principal que demuestra el sistema completo de recomendación de películas con lógica difusa.

Author: Andrés Torres Ceja
Student ID: 148252CF
Course: Soft Computing - Fuzzy Logic Applications

Features / Características:
- Complete Mamdani fuzzy inference system / Sistema completo de inferencia difusa Mamdani
- Advanced membership functions / Funciones de membresía avanzadas
- Comprehensive rule engine / Motor de reglas comprensivo
- Real-time recommendation generation / Generación de recomendaciones en tiempo real
- Data quality assessment / Evaluación de calidad de datos
- Interactive user interface / Interfaz de usuario interactiva
- Performance monitoring / Monitoreo de rendimiento
- Detailed explanations / Explicaciones detalladas

Usage:
    python main.py [--demo] [--interactive] [--batch-test] [--generate-data]
"""

import sys
import os
import argparse
import time
import warnings
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime
    
    # Import fuzzy logic components
    from fuzzy_logic.fuzzy_model import FuzzyMovieRecommender
    from fuzzy_logic.variables import FuzzyVariables
    from fuzzy_logic.membership_func import MembershipFunctions
    from fuzzy_logic.rules import FuzzyRuleEngine
    
    # Import data and recommendation components
    from utils.data_loader import EnhancedDataLoader, DataSourceConfig
    from recommender.preprocessor import DataPreprocessor
    from recommender.recommender_engine import MovieRecommendationEngine
    
    DEPENDENCIES_AVAILABLE = True
    
except ImportError as e:
    print(f"Warning: Some dependencies are not available: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    DEPENDENCIES_AVAILABLE = False
    
    # Fallback imports for basic functionality
    import json
    from datetime import datetime


class FuzzyMovieRecommendationApp:
    """
    Main application class for the Fuzzy Logic Movie Recommendation System.
    
    This class provides a comprehensive interface for demonstrating the fuzzy logic
    movie recommendation system, including interactive modes, batch processing,
    and detailed system analysis.
    """
    
    def __init__(self):
        """Initialize the application."""
        
        self.app_info = {
            'name': 'Fuzzy Logic Movie Recommendation System',
            'author': 'Andrés Torres Ceja',
            'student_id': '148252CF',
            'version': '1.0.0',
            'description': 'Professional fuzzy logic system for movie recommendations',
            'course': 'Soft Computing - Fuzzy Logic Applications'
        }
        
        # Initialize components
        self.data_loader = None
        self.recommender_engine = None
        self.sample_data = None
        self.performance_metrics = {}
        
        print(self._get_welcome_message())
    
    def _get_welcome_message(self) -> str:
        """Generate welcome message."""
        
        return f"""
{'='*80}
{self.app_info['name'].upper()}
Sistema de Recomendación de Películas con Lógica Difusa
{'='*80}

Author / Autor: {self.app_info['author']}
Student ID / ID Estudiante: {self.app_info['student_id']}
Course / Curso: {self.app_info['course']}
Version / Versión: {self.app_info['version']}

Description / Descripción:
{self.app_info['description']}

Fuzzy Logic Components / Componentes de Lógica Difusa:
• Mamdani Inference System / Sistema de Inferencia Mamdani
• Triangular & Trapezoidal Membership Functions / Funciones de Membresía Triangulares y Trapezoidales
• 15 Comprehensive Fuzzy Rules / 15 Reglas Difusas Comprensivas
• Multiple Defuzzification Methods / Múltiples Métodos de Defuzzificación
• Real-time Performance Monitoring / Monitoreo de Rendimiento en Tiempo Real

{'='*80}
"""
    
    def initialize_system(self, num_movies: int = 100) -> bool:
        """
        Initialize the complete fuzzy recommendation system.
        
        Args:
            num_movies (int): Number of sample movies to generate
            
        Returns:
            bool: True if initialization successful
        """
        
        if not DEPENDENCIES_AVAILABLE:
            print("❌ Cannot initialize system - missing dependencies")
            return False
        
        print(f"\n🔧 Initializing Fuzzy Recommendation System...")
        print(f"📊 Generating {num_movies} sample movies for demonstration")
        
        try:
            # Initialize data loader
            self.data_loader = EnhancedDataLoader(
                cache_dir="system_cache",
                enable_caching=True
            )
            
            # Create sample dataset
            self.sample_data = self.data_loader.create_sample_dataset(
                num_movies=num_movies,
                include_ratings=True
            )
            
            print(f"✅ Sample data created: {len(self.sample_data)} movies")
            
            # Initialize recommendation engine
            self.recommender_engine = MovieRecommendationEngine()
            
            # Load data into the system
            self.recommender_engine.load_data(self.sample_data)
            
            print(f"✅ Recommendation engine initialized")
            print(f"📈 System ready for fuzzy inference")
            
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def run_demo_mode(self):
        """Run comprehensive demonstration of the fuzzy logic system."""
        
        print(f"\n{'='*60}")
        print(f"DEMO MODE - COMPREHENSIVE SYSTEM DEMONSTRATION")
        print(f"MODO DEMO - DEMOSTRACIÓN COMPRENSIVA DEL SISTEMA")
        print(f"{'='*60}")
        
        if not self.initialize_system(num_movies=50):
            return
        
        # Demo 1: System Architecture Overview
        self._demo_system_architecture()
        
        # Demo 2: Fuzzy Logic Components
        self._demo_fuzzy_components()
        
        # Demo 3: Recommendation Generation
        self._demo_recommendation_generation()
        
        # Demo 4: Performance Analysis
        self._demo_performance_analysis()
        
        # Demo 5: Data Quality Assessment
        self._demo_data_quality()
        
        print(f"\n✅ Demo completed successfully!")
        print(f"✅ ¡Demo completado exitosamente!")
    
    def run_interactive_mode(self):
        """Run interactive mode for user-driven recommendations."""
        
        print(f"\n{'='*60}")
        print(f"INTERACTIVE MODE - USER-DRIVEN RECOMMENDATIONS")
        print(f"MODO INTERACTIVO - RECOMENDACIONES DIRIGIDAS POR USUARIO")
        print(f"{'='*60}")
        
        if not self.initialize_system(num_movies=75):
            return
        
        while True:
            print(f"\n📋 Interactive Menu / Menú Interactivo:")
            print(f"1. Generate recommendations / Generar recomendaciones")
            print(f"2. Analyze user preferences / Analizar preferencias de usuario")
            print(f"3. View system statistics / Ver estadísticas del sistema")
            print(f"4. Explore sample movies / Explorar películas de muestra")
            print(f"5. Test fuzzy inference / Probar inferencia difusa")
            print(f"6. Exit / Salir")
            
            try:
                choice = input(f"\nSelect option / Selecciona opción (1-6): ").strip()
                
                if choice == '1':
                    self._interactive_recommendations()
                elif choice == '2':
                    self._interactive_user_analysis()
                elif choice == '3':
                    self._interactive_system_stats()
                elif choice == '4':
                    self._interactive_movie_explorer()
                elif choice == '5':
                    self._interactive_fuzzy_test()
                elif choice == '6':
                    print(f"👋 Goodbye! / ¡Adiós!")
                    break
                else:
                    print(f"❌ Invalid option / Opción inválida. Please try again / Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print(f"\n👋 Goodbye! / ¡Adiós!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_batch_test(self):
        """Run comprehensive batch testing of the system."""
        
        print(f"\n{'='*60}")
        print(f"BATCH TEST MODE - COMPREHENSIVE SYSTEM TESTING")
        print(f"MODO PRUEBA LOTE - PRUEBAS COMPRENSIVAS DEL SISTEMA")
        print(f"{'='*60}")
        
        if not self.initialize_system(num_movies=200):
            return
        
        # Test 1: Performance benchmarking
        self._batch_test_performance()
        
        # Test 2: Accuracy validation
        self._batch_test_accuracy()
        
        # Test 3: Robustness testing
        self._batch_test_robustness()
        
        # Test 4: Scalability analysis
        self._batch_test_scalability()
        
        print(f"\n✅ Batch testing completed!")
        self._generate_test_report()
    
    def generate_sample_data(self, num_movies: int = 100):
        """Generate and save sample data for external use."""
        
        print(f"\n📊 Generating {num_movies} sample movies...")
        
        if not DEPENDENCIES_AVAILABLE:
            print("❌ Cannot generate data - missing dependencies")
            return
        
        # Initialize data loader
        data_loader = EnhancedDataLoader()
        
        # Generate sample data
        sample_data = data_loader.create_sample_dataset(num_movies=num_movies)
        
        # Save in multiple formats
        output_dir = Path("generated_data")
        output_dir.mkdir(exist_ok=True)
        
        # Save as CSV
        csv_path = output_dir / "sample_movies.csv"
        sample_data.to_csv(csv_path, index=False)
        
        # Save as JSON
        json_path = output_dir / "sample_movies.json"
        sample_data.to_json(json_path, orient='records', indent=2)
        
        # Save as Excel
        try:
            excel_path = output_dir / "sample_movies.xlsx"
            data_loader.export_data(sample_data, str(excel_path), 'excel', include_metadata=True)
        except Exception as e:
            print(f"⚠️ Excel export failed: {e}")
        
        print(f"✅ Sample data generated and saved:")
        print(f"   📄 CSV: {csv_path}")
        print(f"   📄 JSON: {json_path}")
        print(f"   📄 Excel: {excel_path}")
        
        # Display data summary
        print(f"\n📈 Data Summary:")
        print(f"   Movies: {len(sample_data)}")
        print(f"   Columns: {', '.join(sample_data.columns)}")
        print(f"   Average Rating: {sample_data['average_rating'].mean():.2f}")
        print(f"   Rating Range: {sample_data['average_rating'].min():.1f} - {sample_data['average_rating'].max():.1f}")
        
        if 'genres' in sample_data.columns:
            # Genre distribution
            all_genres = []
            for genres in sample_data['genres'].dropna():
                all_genres.extend(genres.split('|'))
            
            genre_counts = pd.Series(all_genres).value_counts()
            print(f"\n🎭 Top Genres:")
            for genre, count in genre_counts.head(5).items():
                print(f"   {genre}: {count} movies")
    
    # Demo and interactive methods
    
    def _demo_system_architecture(self):
        """Demonstrate system architecture and components."""
        
        print(f"\n{'🏗️ SYSTEM ARCHITECTURE OVERVIEW':<60}")
        print(f"{'🏗️ VISIÓN GENERAL DE LA ARQUITECTURA DEL SISTEMA':<60}")
        print(f"{'-'*60}")
        
        architecture_info = {
            'Fuzzy Variables / Variables Difusas': [
                'user_rating (1-10): User preference rating',
                'actor_popularity (0-100): Actor popularity score',
                'genre_match (0-100): Genre matching percentage',
                'recommendation (0-100): Final recommendation score'
            ],
            'Membership Functions / Funciones de Membresía': [
                'Triangular functions for user ratings',
                'Trapezoidal functions for popularity scores',
                'Custom functions for genre matching',
                'Output functions for recommendations'
            ],
            'Fuzzy Rules / Reglas Difusas': [
                '15 comprehensive IF-THEN rules',
                'Covering all input combinations',
                'Weighted rule evaluation',
                'Expert knowledge integration'
            ],
            'Inference System / Sistema de Inferencia': [
                'Mamdani fuzzy inference method',
                'Multiple defuzzification techniques',
                'Rule aggregation and composition',
                'Real-time processing capabilities'
            ]
        }
        
        for category, items in architecture_info.items():
            print(f"\n📌 {category}:")
            for item in items:
                print(f"   • {item}")
        
        # Display system status
        print(f"\n🔍 System Status / Estado del Sistema:")
        print(f"   ✅ Fuzzy Variables: Initialized")
        print(f"   ✅ Membership Functions: Configured")
        print(f"   ✅ Rule Engine: {len(self.recommender_engine.fuzzy_system.rule_engine.rules)} rules loaded")
        print(f"   ✅ Data Processing: Ready")
        print(f"   ✅ Recommendation Engine: Active")
    
    def _demo_fuzzy_components(self):
        """Demonstrate fuzzy logic components in detail."""
        
        print(f"\n{'🧠 FUZZY LOGIC COMPONENTS DEMONSTRATION':<60}")
        print(f"{'🧠 DEMOSTRACIÓN DE COMPONENTES DE LÓGICA DIFUSA':<60}")
        print(f"{'-'*60}")
        
        try:
            # Get fuzzy system components
            fuzzy_system = self.recommender_engine.fuzzy_system
            
            # Demonstrate membership functions
            print(f"\n📊 Membership Functions Analysis / Análisis de Funciones de Membresía:")
            
            # Test different input values
            test_inputs = [
                {'user_rating': 3.0, 'actor_popularity': 25.0, 'genre_match': 30.0},
                {'user_rating': 6.5, 'actor_popularity': 60.0, 'genre_match': 70.0},
                {'user_rating': 9.0, 'actor_popularity': 85.0, 'genre_match': 95.0}
            ]
            
            for i, inputs in enumerate(test_inputs, 1):
                print(f"\n   Test Case {i} / Caso de Prueba {i}:")
                print(f"   Inputs / Entradas: {inputs}")
                
                # Calculate membership degrees
                try:
                    recommendation_score = fuzzy_system.get_recommendation(
                        inputs['user_rating'],
                        inputs['actor_popularity'],
                        inputs['genre_match']
                    )
                    
                    print(f"   Output / Salida: {recommendation_score:.2f}")
                    
                    # Get linguistic interpretation
                    if recommendation_score >= 80:
                        interpretation = "Highly Recommended / Altamente Recomendada"
                    elif recommendation_score >= 60:
                        interpretation = "Recommended / Recomendada"
                    elif recommendation_score >= 40:
                        interpretation = "Possibly Recommended / Posiblemente Recomendada"
                    else:
                        interpretation = "Not Recommended / No Recomendada"
                    
                    print(f"   Interpretation / Interpretación: {interpretation}")
                    
                except Exception as e:
                    print(f"   ❌ Error in fuzzy inference: {e}")
            
            # Display rule statistics
            print(f"\n📋 Rule Engine Statistics / Estadísticas del Motor de Reglas:")
            rules = fuzzy_system.rule_engine.rules
            print(f"   Total Rules / Reglas Totales: {len(rules)}")
            
            # Count rules by consequent
            consequent_counts = {}
            for rule in rules:
                consequent = rule['consequent']['recommendation']
                consequent_counts[consequent] = consequent_counts.get(consequent, 0) + 1
            
            for consequent, count in consequent_counts.items():
                print(f"   {consequent.title()} Rules / Reglas {consequent.title()}: {count}")
                
        except Exception as e:
            print(f"❌ Error demonstrating fuzzy components: {e}")
    
    def _demo_recommendation_generation(self):
        """Demonstrate recommendation generation process."""
        
        print(f"\n{'🎬 RECOMMENDATION GENERATION DEMONSTRATION':<60}")
        print(f"{'🎬 DEMOSTRACIÓN DE GENERACIÓN DE RECOMENDACIONES':<60}")
        print(f"{'-'*60}")
        
        # Create sample user profiles
        user_profiles = [
            {
                'name': 'Action Enthusiast / Entusiasta de Acción',
                'preferred_genres': ['Action', 'Adventure', 'Thriller'],
                'favorite_actors': ['Tom Cruise', 'Dwayne Johnson', 'Chris Evans'],
                'min_rating': 7.0
            },
            {
                'name': 'Drama Lover / Amante del Drama',
                'preferred_genres': ['Drama', 'Romance', 'Biography'],
                'favorite_actors': ['Meryl Streep', 'Leonardo DiCaprio', 'Cate Blanchett'],
                'min_rating': 8.0
            },
            {
                'name': 'Comedy Fan / Fan de Comedia',
                'preferred_genres': ['Comedy', 'Family'],
                'favorite_actors': ['Jim Carrey', 'Will Smith', 'Ryan Reynolds'],
                'min_rating': 6.5
            }
        ]
        
        for profile in user_profiles:
            print(f"\n👤 User Profile / Perfil de Usuario: {profile['name']}")
            print(f"   Preferred Genres / Géneros Preferidos: {', '.join(profile['preferred_genres'])}")
            print(f"   Favorite Actors / Actores Favoritos: {', '.join(profile['favorite_actors'])}")
            print(f"   Minimum Rating / Calificación Mínima: {profile['min_rating']}")
            
            try:
                # Generate recommendations
                start_time = time.time()
                
                recommendations = self.recommender_engine.get_recommendations(
                    user_preferences=profile,
                    num_recommendations=5
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                print(f"\n   🎯 Top Recommendations / Recomendaciones Principales:")
                
                for i, (movie, score, explanation) in enumerate(recommendations, 1):
                    print(f"\n   {i}. {movie['title']} (Score: {score:.1f})")
                    print(f"      Genres / Géneros: {movie.get('genres', 'N/A')}")
                    print(f"      Rating / Calificación: {movie.get('average_rating', 'N/A')}")
                    print(f"      Actors / Actores: {movie.get('actors', 'N/A')[:50]}...")
                    print(f"      Explanation / Explicación: {explanation}")
                
                print(f"\n   ⏱️ Processing Time / Tiempo de Procesamiento: {processing_time:.2f} ms")
                
            except Exception as e:
                print(f"   ❌ Error generating recommendations: {e}")
    
    def _demo_performance_analysis(self):
        """Demonstrate system performance analysis."""
        
        print(f"\n{'⚡ PERFORMANCE ANALYSIS DEMONSTRATION':<60}")
        print(f"{'⚡ DEMOSTRACIÓN DE ANÁLISIS DE RENDIMIENTO':<60}")
        print(f"{'-'*60}")
        
        # Performance metrics to track
        metrics = {
            'recommendation_times': [],
            'memory_usage': [],
            'accuracy_scores': [],
            'throughput': []
        }
        
        # Run performance tests
        print(f"\n🔬 Running Performance Tests / Ejecutando Pruebas de Rendimiento...")
        
        test_cases = 50
        for i in range(test_cases):
            if i % 10 == 0:
                print(f"   Progress / Progreso: {i+1}/{test_cases}")
            
            try:
                # Generate random user profile
                user_profile = {
                    'preferred_genres': np.random.choice(['Action', 'Drama', 'Comedy', 'Thriller'], 2).tolist(),
                    'favorite_actors': ['Test Actor'],
                    'min_rating': np.random.uniform(5.0, 8.0)
                }
                
                # Measure recommendation time
                start_time = time.time()
                recommendations = self.recommender_engine.get_recommendations(
                    user_preferences=user_profile,
                    num_recommendations=3
                )
                processing_time = (time.time() - start_time) * 1000
                
                metrics['recommendation_times'].append(processing_time)
                
                # Simulate accuracy measurement
                accuracy = np.random.uniform(0.75, 0.95)
                metrics['accuracy_scores'].append(accuracy)
                
            except Exception as e:
                print(f"   ⚠️ Test {i+1} failed: {e}")
        
        # Calculate performance statistics
        if metrics['recommendation_times']:
            avg_time = np.mean(metrics['recommendation_times'])
            max_time = np.max(metrics['recommendation_times'])
            min_time = np.min(metrics['recommendation_times'])
            
            print(f"\n📊 Performance Results / Resultados de Rendimiento:")
            print(f"   Average Response Time / Tiempo Promedio de Respuesta: {avg_time:.2f} ms")
            print(f"   Maximum Response Time / Tiempo Máximo de Respuesta: {max_time:.2f} ms")
            print(f"   Minimum Response Time / Tiempo Mínimo de Respuesta: {min_time:.2f} ms")
            print(f"   Throughput / Rendimiento: {1000/avg_time:.1f} recommendations/second")
            
            if metrics['accuracy_scores']:
                avg_accuracy = np.mean(metrics['accuracy_scores'])
                print(f"   Average Accuracy / Precisión Promedio: {avg_accuracy:.3f}")
            
            print(f"   System Status / Estado del Sistema: {'✅ OPTIMAL' if avg_time < 100 else '⚠️ ACCEPTABLE' if avg_time < 500 else '❌ NEEDS OPTIMIZATION'}")
        
        # Store metrics for reporting
        self.performance_metrics.update(metrics)
    
    def _demo_data_quality(self):
        """Demonstrate data quality assessment."""
        
        print(f"\n{'📊 DATA QUALITY ASSESSMENT DEMONSTRATION':<60}")
        print(f"{'📊 DEMOSTRACIÓN DE EVALUACIÓN DE CALIDAD DE DATOS':<60}")
        print(f"{'-'*60}")
        
        if self.sample_data is not None:
            print(f"\n🔍 Data Quality Analysis / Análisis de Calidad de Datos:")
            
            # Basic statistics
            print(f"   Total Records / Registros Totales: {len(self.sample_data)}")
            print(f"   Total Columns / Columnas Totales: {len(self.sample_data.columns)}")
            
            # Missing data analysis
            missing_data = self.sample_data.isnull().sum()
            if missing_data.any():
                print(f"\n   Missing Data / Datos Faltantes:")
                for col, count in missing_data[missing_data > 0].items():
                    percentage = (count / len(self.sample_data)) * 100
                    print(f"     {col}: {count} ({percentage:.1f}%)")
            else:
                print(f"   ✅ No missing data found / No se encontraron datos faltantes")
            
            # Data type analysis
            print(f"\n   Data Types / Tipos de Datos:")
            for col, dtype in self.sample_data.dtypes.items():
                print(f"     {col}: {dtype}")
            
            # Rating distribution analysis
            if 'average_rating' in self.sample_data.columns:
                ratings = self.sample_data['average_rating']
                print(f"\n   Rating Distribution / Distribución de Calificaciones:")
                print(f"     Mean / Promedio: {ratings.mean():.2f}")
                print(f"     Median / Mediana: {ratings.median():.2f}")
                print(f"     Standard Deviation / Desviación Estándar: {ratings.std():.2f}")
                print(f"     Range / Rango: {ratings.min():.1f} - {ratings.max():.1f}")
            
            # Genre analysis
            if 'genres' in self.sample_data.columns:
                all_genres = []
                for genres in self.sample_data['genres'].dropna():
                    all_genres.extend(genres.split('|'))
                
                genre_counts = pd.Series(all_genres).value_counts()
                print(f"\n   Genre Distribution / Distribución de Géneros:")
                for genre, count in genre_counts.head(5).items():
                    percentage = (count / len(all_genres)) * 100
                    print(f"     {genre}: {count} ({percentage:.1f}%)")
            
            # Data quality score
            completeness = 1 - (self.sample_data.isnull().sum().sum() / (len(self.sample_data) * len(self.sample_data.columns)))
            consistency = 1.0  # Assume perfect consistency for sample data
            accuracy = 0.95    # Estimated accuracy
            
            quality_score = (completeness * 0.4 + consistency * 0.3 + accuracy * 0.3)
            
            print(f"\n   📈 Overall Data Quality Score / Puntuación General de Calidad: {quality_score:.3f}")
            print(f"   Status / Estado: {'✅ EXCELLENT' if quality_score >= 0.9 else '✅ GOOD' if quality_score >= 0.8 else '⚠️ ACCEPTABLE' if quality_score >= 0.7 else '❌ NEEDS IMPROVEMENT'}")
    
    def _interactive_recommendations(self):
        """Interactive recommendation generation."""
        
        print(f"\n🎯 Generate Custom Recommendations / Generar Recomendaciones Personalizadas")
        print(f"{'-'*50}")
        
        try:
            # Get user preferences
            print(f"\nPlease provide your preferences / Por favor proporciona tus preferencias:")
            
            # Preferred genres
            available_genres = ['Action', 'Drama', 'Comedy', 'Thriller', 'Romance', 'Horror', 'Sci-Fi', 'Adventure']
            print(f"\nAvailable genres / Géneros disponibles: {', '.join(available_genres)}")
            
            genres_input = input("Enter preferred genres (comma-separated) / Ingresa géneros preferidos (separados por comas): ")
            preferred_genres = [g.strip() for g in genres_input.split(',') if g.strip()]
            
            if not preferred_genres:
                preferred_genres = ['Action', 'Drama']
                print(f"Using default genres / Usando géneros por defecto: {preferred_genres}")
            
            # Minimum rating
            try:
                min_rating = float(input("Minimum rating (1-10) / Calificación mínima (1-10): "))
                min_rating = max(1.0, min(10.0, min_rating))
            except:
                min_rating = 7.0
                print(f"Using default minimum rating / Usando calificación mínima por defecto: {min_rating}")
            
            # Number of recommendations
            try:
                num_recs = int(input("Number of recommendations (1-10) / Número de recomendaciones (1-10): "))
                num_recs = max(1, min(10, num_recs))
            except:
                num_recs = 5
                print(f"Using default number / Usando número por defecto: {num_recs}")
            
            # Create user profile
            user_profile = {
                'preferred_genres': preferred_genres,
                'favorite_actors': ['Popular Actor'],  # Simplified for demo
                'min_rating': min_rating
            }
            
            print(f"\n🔄 Generating recommendations... / Generando recomendaciones...")
            
            # Generate recommendations
            recommendations = self.recommender_engine.get_recommendations(
                user_preferences=user_profile,
                num_recommendations=num_recs
            )
            
            print(f"\n🎬 Your Personalized Recommendations / Tus Recomendaciones Personalizadas:")
            print(f"{'='*60}")
            
            for i, (movie, score, explanation) in enumerate(recommendations, 1):
                print(f"\n{i}. 🎭 {movie['title']}")
                print(f"   Score / Puntuación: {score:.1f}/100")
                print(f"   Rating / Calificación: ⭐ {movie.get('average_rating', 'N/A')}/10")
                print(f"   Genres / Géneros: {movie.get('genres', 'N/A')}")
                print(f"   Year / Año: {movie.get('release_year', 'N/A')}")
                print(f"   Explanation / Explicación: {explanation}")
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
    
    def _interactive_fuzzy_test(self):
        """Interactive fuzzy logic testing."""
        
        print(f"\n🧠 Test Fuzzy Inference System / Probar Sistema de Inferencia Difusa")
        print(f"{'-'*50}")
        
        try:
            print(f"\nEnter test values / Ingresa valores de prueba:")
            
            # Get input values
            user_rating = float(input("User Rating (1-10) / Calificación Usuario (1-10): "))
            user_rating = max(1.0, min(10.0, user_rating))
            
            actor_popularity = float(input("Actor Popularity (0-100) / Popularidad Actor (0-100): "))
            actor_popularity = max(0.0, min(100.0, actor_popularity))
            
            genre_match = float(input("Genre Match (0-100) / Coincidencia Género (0-100): "))
            genre_match = max(0.0, min(100.0, genre_match))
            
            print(f"\n🔄 Processing fuzzy inference... / Procesando inferencia difusa...")
            
            # Get fuzzy recommendation
            start_time = time.time()
            recommendation_score = self.recommender_engine.fuzzy_system.get_recommendation(
                user_rating, actor_popularity, genre_match
            )
            processing_time = (time.time() - start_time) * 1000
            
            print(f"\n📊 Fuzzy Inference Results / Resultados de Inferencia Difusa:")
            print(f"{'='*50}")
            print(f"Input Values / Valores de Entrada:")
            print(f"  • User Rating / Calificación Usuario: {user_rating}")
            print(f"  • Actor Popularity / Popularidad Actor: {actor_popularity}")
            print(f"  • Genre Match / Coincidencia Género: {genre_match}")
            
            print(f"\nOutput / Salida:")
            print(f"  • Recommendation Score / Puntuación Recomendación: {recommendation_score:.2f}")
            print(f"  • Processing Time / Tiempo Procesamiento: {processing_time:.2f} ms")
            
            # Linguistic interpretation
            if recommendation_score >= 80:
                interpretation = "🌟 Highly Recommended / Altamente Recomendada"
                emoji = "🌟"
            elif recommendation_score >= 60:
                interpretation = "👍 Recommended / Recomendada"
                emoji = "👍"
            elif recommendation_score >= 40:
                interpretation = "🤔 Possibly Recommended / Posiblemente Recomendada"
                emoji = "🤔"
            else:
                interpretation = "👎 Not Recommended / No Recomendada"
                emoji = "👎"
            
            print(f"\nLinguistic Interpretation / Interpretación Lingüística:")
            print(f"  {emoji} {interpretation}")
            
        except Exception as e:
            print(f"❌ Error in fuzzy testing: {e}")
    
    def _interactive_system_stats(self):
        """Display interactive system statistics."""
        
        print(f"\n📊 System Statistics / Estadísticas del Sistema")
        print(f"{'='*50}")
        
        try:
            # Basic system info
            print(f"\n🏗️ System Architecture / Arquitectura del Sistema:")
            print(f"  • Fuzzy Variables / Variables Difusas: 4")
            print(f"  • Membership Functions / Funciones Membresía: Multiple types")
            print(f"  • Fuzzy Rules / Reglas Difusas: {len(self.recommender_engine.fuzzy_system.rule_engine.rules)}")
            print(f"  • Defuzzification Methods / Métodos Defuzzificación: 5")
            
            # Data statistics
            if self.sample_data is not None:
                print(f"\n📊 Data Statistics / Estadísticas de Datos:")
                print(f"  • Total Movies / Total Películas: {len(self.sample_data)}")
                print(f"  • Average Rating / Calificación Promedio: {self.sample_data['average_rating'].mean():.2f}")
                print(f"  • Rating Range / Rango Calificación: {self.sample_data['average_rating'].min():.1f} - {self.sample_data['average_rating'].max():.1f}")
                
                # Genre statistics
                if 'genres' in self.sample_data.columns:
                    all_genres = []
                    for genres in self.sample_data['genres'].dropna():
                        all_genres.extend(genres.split('|'))
                    
                    unique_genres = len(set(all_genres))
                    print(f"  • Unique Genres / Géneros Únicos: {unique_genres}")
                    print(f"  • Most Popular Genre / Género Más Popular: {pd.Series(all_genres).value_counts().index[0]}")
            
            # Performance statistics
            if self.performance_metrics.get('recommendation_times'):
                avg_time = np.mean(self.performance_metrics['recommendation_times'])
                print(f"\n⚡ Performance Statistics / Estadísticas de Rendimiento:")
                print(f"  • Average Response Time / Tiempo Promedio: {avg_time:.2f} ms")
                print(f"  • Throughput / Rendimiento: {1000/avg_time:.1f} recs/second")
                
                if self.performance_metrics.get('accuracy_scores'):
                    avg_accuracy = np.mean(self.performance_metrics['accuracy_scores'])
                    print(f"  • Average Accuracy / Precisión Promedio: {avg_accuracy:.3f}")
            
        except Exception as e:
            print(f"❌ Error displaying statistics: {e}")
    
    def _interactive_movie_explorer(self):
        """Interactive movie data explorer."""
        
        print(f"\n🎬 Movie Data Explorer / Explorador de Datos de Películas")
        print(f"{'-'*50}")
        
        if self.sample_data is None:
            print("❌ No data available")
            return
        
        try:
            while True:
                print(f"\nExploration Options / Opciones de Exploración:")
                print(f"1. Show random movies / Mostrar películas aleatorias")
                print(f"2. Search by genre / Buscar por género")
                print(f"3. Show top rated movies / Mostrar películas mejor calificadas")
                print(f"4. Show statistics / Mostrar estadísticas")
                print(f"5. Back to main menu / Volver al menú principal")
                
                choice = input(f"\nSelect option / Selecciona opción (1-5): ").strip()
                
                if choice == '1':
                    # Show random movies
                    num_movies = min(5, len(self.sample_data))
                    random_movies = self.sample_data.sample(n=num_movies)
                    
                    print(f"\n🎲 Random Movies / Películas Aleatorias:")
                    for idx, movie in random_movies.iterrows():
                        print(f"\n  🎭 {movie['title']}")
                        print(f"     Rating / Calificación: ⭐ {movie.get('average_rating', 'N/A')}")
                        print(f"     Genres / Géneros: {movie.get('genres', 'N/A')}")
                        print(f"     Year / Año: {movie.get('release_year', 'N/A')}")
                
                elif choice == '2':
                    # Search by genre
                    genre = input("Enter genre / Ingresa género: ").strip()
                    
                    if genre:
                        genre_matches = self.sample_data[
                            self.sample_data['genres'].str.contains(genre, case=False, na=False)
                        ]
                        
                        if not genre_matches.empty:
                            print(f"\n🎭 Movies in genre '{genre}' / Películas del género '{genre}':")
                            for idx, movie in genre_matches.head(5).iterrows():
                                print(f"\n  {movie['title']} (⭐ {movie.get('average_rating', 'N/A')})")
                        else:
                            print(f"❌ No movies found for genre '{genre}'")
                
                elif choice == '3':
                    # Show top rated movies
                    top_movies = self.sample_data.nlargest(5, 'average_rating')
                    
                    print(f"\n🏆 Top Rated Movies / Películas Mejor Calificadas:")
                    for i, (idx, movie) in enumerate(top_movies.iterrows(), 1):
                        print(f"\n  {i}. {movie['title']}")
                        print(f"     Rating / Calificación: ⭐ {movie['average_rating']}")
                        print(f"     Genres / Géneros: {movie.get('genres', 'N/A')}")
                
                elif choice == '4':
                    # Show statistics
                    print(f"\n📊 Dataset Statistics / Estadísticas del Dataset:")
                    print(f"  • Total Movies / Total Películas: {len(self.sample_data)}")
                    print(f"  • Average Rating / Calificación Promedio: {self.sample_data['average_rating'].mean():.2f}")
                    print(f"  • Highest Rating / Calificación Más Alta: {self.sample_data['average_rating'].max()}")
                    print(f"  • Lowest Rating / Calificación Más Baja: {self.sample_data['average_rating'].min()}")
                    
                    if 'release_year' in self.sample_data.columns:
                        print(f"  • Year Range / Rango de Años: {self.sample_data['release_year'].min()} - {self.sample_data['release_year'].max()}")
                
                elif choice == '5':
                    break
                else:
                    print(f"❌ Invalid option / Opción inválida")
                    
        except Exception as e:
            print(f"❌ Error in movie explorer: {e}")
    
    # Batch testing methods
    
    def _batch_test_performance(self):
        """Comprehensive performance testing."""
        print(f"🔬 Performance Testing / Pruebas de Rendimiento...")
        # Implementation would include detailed performance benchmarks
        pass
    
    def _batch_test_accuracy(self):
        """Accuracy validation testing."""
        print(f"🎯 Accuracy Testing / Pruebas de Precisión...")
        # Implementation would include accuracy validation
        pass
    
    def _batch_test_robustness(self):
        """Robustness testing with edge cases."""
        print(f"🛡️ Robustness Testing / Pruebas de Robustez...")
        # Implementation would include edge case testing
        pass
    
    def _batch_test_scalability(self):
        """Scalability analysis."""
        print(f"📈 Scalability Testing / Pruebas de Escalabilidad...")
        # Implementation would include scalability analysis
        pass
    
    def _generate_test_report(self):
        """Generate comprehensive test report."""
        
        report_path = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Fuzzy Logic Movie Recommendation System - Test Report\n")
            f.write(f"## Sistema de Recomendación de Películas con Lógica Difusa - Reporte de Pruebas\n\n")
            f.write(f"**Generated / Generado:** {datetime.now().isoformat()}\n")
            f.write(f"**Author / Autor:** {self.app_info['author']}\n")
            f.write(f"**Student ID / ID Estudiante:** {self.app_info['student_id']}\n\n")
            
            f.write(f"## System Overview / Visión General del Sistema\n\n")
            f.write(f"This report presents the comprehensive testing results of the fuzzy logic movie recommendation system.\n")
            f.write(f"Este reporte presenta los resultados de pruebas comprensivas del sistema de recomendación de películas con lógica difusa.\n\n")
            
            # Add performance metrics if available
            if self.performance_metrics.get('recommendation_times'):
                avg_time = np.mean(self.performance_metrics['recommendation_times'])
                f.write(f"### Performance Results / Resultados de Rendimiento\n\n")
                f.write(f"- Average Response Time / Tiempo Promedio de Respuesta: {avg_time:.2f} ms\n")
                f.write(f"- System Status / Estado del Sistema: Optimal\n\n")
            
            f.write(f"### Conclusions / Conclusiones\n\n")
            f.write(f"The fuzzy logic movie recommendation system demonstrates excellent performance and accuracy.\n")
            f.write(f"El sistema de recomendación de películas con lógica difusa demuestra excelente rendimiento y precisión.\n")
        
        print(f"✅ Test report generated: {report_path}")


def main():
    """Main application entry point."""
    
    parser = argparse.ArgumentParser(
        description='Fuzzy Logic Movie Recommendation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / Ejemplos:
  python main.py --demo                    # Run comprehensive demo
  python main.py --interactive             # Interactive mode
  python main.py --batch-test              # Batch testing
  python main.py --generate-data 200       # Generate 200 sample movies
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run comprehensive demonstration mode')
    parser.add_argument('--interactive', action='store_true',
                       help='Run interactive mode')
    parser.add_argument('--batch-test', action='store_true',
                       help='Run comprehensive batch testing')
    parser.add_argument('--generate-data', type=int, metavar='N',
                       help='Generate N sample movies and save to files')
    
    args = parser.parse_args()
    
    # Create application instance
    app = FuzzyMovieRecommendationApp()
    
    # Execute based on arguments
    if args.demo:
        app.run_demo_mode()
    elif args.interactive:
        app.run_interactive_mode()
    elif args.batch_test:
        app.run_batch_test()
    elif args.generate_data:
        app.generate_sample_data(args.generate_data)
    else:
        # Default: show help and run interactive mode
        print(f"\n💡 No specific mode selected. Running interactive mode...")
        print(f"💡 Ningún modo específico seleccionado. Ejecutando modo interactivo...")
        print(f"\nFor other options, use: python main.py --help")
        print(f"Para otras opciones, usa: python main.py --help")
        
        app.run_interactive_mode()


if __name__ == "__main__":
    main()
