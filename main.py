"""
Fuzzy Logic Movie Recommendation System - Modern Application

A professional fuzzy logic system for movie recommendations with clean visualization.

Author: Andrés Torres Ceja
Student ID: 148252CF
Course: Soft Computing - Universidad de Guanajuato
Version: 2.0.0 (Modernized UI)

Features:
- Mamdani Fuzzy Inference System
- Interactive Visual Interface
- Membership Function Visualization
- Real-time Inference Display
- Clean, Professional Output

Usage:
    python main.py                  # Interactive mode
    python main.py --demo           # Demonstration mode
    python main.py --visualize      # Generate all visualizations
"""

import sys
import os
import argparse
import time
import warnings
import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Suppress warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARNING)

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    import numpy as np
    import pandas as pd
    
    # Core components
    from fuzzy_logic.fuzzy_model import FuzzyMovieRecommender
    from fuzzy_logic.variables import FuzzyVariables
    from utils.data_loader import EnhancedDataLoader
    from recommender.recommender_engine import MovieRecommendationEngine
    
    # Modern UI components
    from ui.interface import UIManager, Colors
    from ui.visualizer import FuzzyVisualizer
    
    DEPS_OK = True
except ImportError as e:
    print(f"ERROR: Missing dependencies - {e}")
    print("Install: pip install -r requirements.txt")
    sys.exit(1)


class ModernFuzzyApp:
    """Modern Fuzzy Logic Movie Recommendation Application."""
    
    def __init__(self):
        """Initialize the modern application."""
        self.ui = UIManager(use_colors=True, width=90)
        self.viz = FuzzyVisualizer(output_dir="visualizations")
        
        self.data_loader = None
        self.engine = None
        self.movies_df = None
        self.fuzzy_vars = None
        
        # Paths
        self.data_dir = Path("data")
        self.generated_data_dir = Path("generated_data")
        self.history_file = self.data_dir / "recommendation_history.json"
        
        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.generated_data_dir.mkdir(exist_ok=True)
        
        # Recommendation history
        self.recommendation_history = self._load_history()
        
        # App metadata
        self.info = {
            'title': 'FUZZY LOGIC MOVIE RECOMMENDATION SYSTEM',
            'author': 'Andrés Torres Ceja',
            'id': '148252CF',
            'version': '2.0.0',
            'course': 'Soft Computing - Universidad de Guanajuato'
        }
    
    def initialize_system(self, num_movies: int = 50, verbose: bool = False):
        """Initialize the recommendation system."""
        if not verbose:
            self.ui.print_info("Initializing Fuzzy Recommendation System...")
        
        try:
            # Load data
            self.data_loader = EnhancedDataLoader(enable_caching=True)
            self.movies_df = self.data_loader.create_sample_dataset(num_movies)
            
            if verbose:
                self.ui.print_success(f"Loaded {len(self.movies_df)} movies")
            
            # Load and merge custom movies if they exist
            custom_file = self.data_dir / "custom_movies.csv"
            if custom_file.exists():
                try:
                    custom_df = pd.read_csv(custom_file)
                    if len(custom_df) > 0:
                        # Fix column name mismatch: main_actors -> actors
                        if 'main_actors' in custom_df.columns and 'actors' not in custom_df.columns:
                            custom_df = custom_df.rename(columns={'main_actors': 'actors'})
                        
                        # Merge custom movies with generated dataset
                        self.movies_df = pd.concat([self.movies_df, custom_df], ignore_index=True)
                        if verbose:
                            self.ui.print_success(f"Loaded {len(custom_df)} custom movies")
                except Exception as e:
                    if verbose:
                        self.ui.print_warning(f"Could not load custom movies: {e}")
            
            # Initialize engine
            self.engine = MovieRecommendationEngine(defuzzification_method='centroid')
            self.engine.initialize_system(self.movies_df)
            
            # Get fuzzy variables reference
            self.fuzzy_vars = self.engine.fuzzy_recommender.fuzzy_variables
            
            if verbose:
                self.ui.print_success("System initialized successfully")
                self.ui.print_key_value({
                    'Movies': len(self.movies_df),
                    'Fuzzy Rules': len(self.engine.fuzzy_recommender.rule_engine.rules),
                    'Variables': 4,
                    'Inference': 'Mamdani'
                })
            
            return True
            
        except Exception as e:
            self.ui.print_error(f"Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_interactive_mode(self):
        """Run interactive mode with clean UI."""
        self.ui.clear_screen()
        self.ui.print_header(self.info['title'], 
                            f"v{self.info['version']} | {self.info['author']}")
        
        if not self.initialize_system(num_movies=75, verbose=True):
            return
        
        while True:
            options = [
                "Generate Movie Recommendations",
                "Visualize Fuzzy Logic System",
                "Analyze User Preferences",
                "View System Dashboard",
                "Explore Movie Database",
                "Test Fuzzy Inference",
                "Add Custom Movie",                    # NEW
                "Export Current Dataset",              # NEW
                "View Recommendation History",          # NEW
                "Generate Sample Dataset",              # NEW
                "Manage Datasets",                      # NEW
                "View Dataset Info",                    # NEW v2.1.2
                "Exit"
            ]
            
            choice = self.ui.print_menu("MAIN MENU", options)
            
            if choice == '1':
                self._generate_recommendations_ui()
            elif choice == '2':
                self._visualize_system_ui()
            elif choice == '3':
                self._analyze_preferences_ui()
            elif choice == '4':
                self._show_dashboard_ui()
            elif choice == '5':
                self._explore_database_ui()
            elif choice == '6':
                self._test_inference_ui()
            elif choice == '7':
                self._add_custom_movie_ui()
            elif choice == '8':
                self._export_dataset_ui()
            elif choice == '9':
                self._view_history_ui()
            elif choice == '10':
                self._generate_sample_dataset_ui()
            elif choice == '11':
                self._manage_datasets_ui()
            elif choice == '12':
                self._view_dataset_info_ui()
            elif choice == '13':
                self._save_history()
                self.ui.print_success("Thank you for using the system!")
                break
            else:
                self.ui.print_warning("Invalid option. Please try again.")
    
    def _generate_recommendations_ui(self):
        """Generate recommendations with clean UI."""
        self.ui.clear_screen()
        self.ui.print_section("MOVIE RECOMMENDATION GENERATOR")
        
        # Get user preferences
        self.ui.print_info("Please provide your preferences:")
        print()
        
        # Show available genres
        available_genres = self._get_available_genres()
        if available_genres:
            self.ui.print_info(f"Available genres: {', '.join(available_genres[:15])}...")
            print()
        
        genres_input = self.ui.input_styled(
            "Preferred genres (comma-separated)", 
            "Action, Drama"
        )
        genres = [g.strip() for g in genres_input.split(',')]
        
        min_rating = self.ui.input_styled("Minimum rating (1-10)", "7.0")
        try:
            min_rating = float(min_rating)
        except:
            min_rating = 7.0
        
        num_recs = self.ui.input_styled("Number of recommendations (1-10)", "5")
        try:
            num_recs = int(num_recs)
        except:
            num_recs = 5
        
        # Generate recommendations
        print()
        self.ui.print_info("Processing fuzzy inference...")
        
        user_prefs = {
            'preferred_genres': genres,
            'favorite_actors': [],
            'min_rating': min_rating
        }
        
        try:
            recommendations = self.engine.get_recommendations(
                user_preferences=user_prefs,
                num_recommendations=num_recs
            )
            
            # Display results
            print()
            self.ui.print_section("RECOMMENDATION RESULTS")
            
            headers = ["#", "Title", "Score", "Rating", "Match%", "Fuzzy", "Genres"]
            rows = []
            
            for i, (movie, score, explanation) in enumerate(recommendations, 1):
                match_score = movie.get('genre_match_score', 0)
                fuzzy_label, visual_indicator = self._get_fuzzy_label(score)
                rows.append([
                    str(i),
                    movie['title'][:30],
                    f"{score:.1f}/100",
                    f"{movie.get('average_rating', 0):.1f}/10",
                    f"{match_score:.0f}%",
                    visual_indicator,
                    movie.get('genres', 'N/A')[:20]
                ])
            
            self.ui.print_table(headers, rows, "Top Recommendations")
            
            # Save to history (save top recommendation)
            if recommendations:
                top_movie, top_score, _ = recommendations[0]
                self._add_to_history(
                    inputs={
                        'user_rating': min_rating,
                        'preferred_genres': genres,
                        'actor_popularity': 50.0,  # Default
                        'genre_match': 70.0  # Default
                    },
                    output=top_score,
                    movie_title=top_movie['title']
                )
            
            # Generate visualizations
            self.ui.print_info("Generating visualizations...")
            
            # 1. Recommendations bar chart
            rec_dicts = []
            for movie, score, _ in recommendations:
                rec_dicts.append({
                    'title': movie['title'],
                    'score': score,
                    'average_rating': movie.get('average_rating', 0)
                })
            
            viz_path = self.viz.plot_recommendations(rec_dicts, show=False)
            self.ui.print_success(f"Recommendations chart: {viz_path}")
            
            # 2. Fuzzy membership functions with recommendation scores
            membership_path = self._plot_membership_with_scores(recommendations)
            if membership_path:
                self.ui.print_success(f"Membership functions: {membership_path}")
            
        except Exception as e:
            self.ui.print_error(f"Error generating recommendations: {e}")
        
        self.ui.wait_for_user()
    
    def _plot_membership_with_scores(self, recommendations: List[Tuple]) -> Optional[str]:
        """
        Plot fuzzy membership functions with vertical lines showing where recommendations fall.
        
        Args:
            recommendations: List of (movie_dict, score, explanation) tuples
            
        Returns:
            Path to saved plot or None if error
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            import skfuzzy as fuzz
            
            # Prepare data
            scores = [score for _, score, _ in recommendations[:5]]  # Top 5
            titles = [movie['title'][:15] for movie, _, _ in recommendations[:5]]
            
            # Universe of discourse
            universe = np.arange(0, 101, 1)
            
            # Define membership functions (matching variables.py)
            not_rec = fuzz.trimf(universe, [0, 0, 25])
            possibly = fuzz.trimf(universe, [15, 40, 65])
            recommended = fuzz.trimf(universe, [50, 75, 90])
            highly = fuzz.trimf(universe, [80, 100, 100])
            
            # Create figure
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Plot membership functions with distinct colors
            ax.plot(universe, not_rec, 'r-', linewidth=2.5, label='Not Recommended', alpha=0.8)
            ax.plot(universe, possibly, 'orange', linewidth=2.5, label='Possibly Recommended', alpha=0.8)
            ax.plot(universe, recommended, 'gold', linewidth=2.5, label='Recommended', alpha=0.8)
            ax.plot(universe, highly, 'g-', linewidth=2.5, label='Highly Recommended', alpha=0.8)
            
            # Plot vertical lines for each recommendation
            colors_for_lines = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            for i, (score, title) in enumerate(zip(scores, titles)):
                color = colors_for_lines[i % len(colors_for_lines)]
                ax.axvline(x=score, color=color, linestyle='--', linewidth=2, alpha=0.7)
                
                # Add label at top
                ax.text(score, 1.05, f'{title}\n({score:.1f})', 
                       rotation=45, ha='left', va='bottom',
                       fontsize=9, color=color, fontweight='bold')
            
            # Styling
            ax.set_xlabel('Recommendation Score', fontsize=12, fontweight='bold')
            ax.set_ylabel('Membership Degree', fontsize=12, fontweight='bold')
            ax.set_title('Fuzzy Membership Functions - Recommendation Output Variable', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.set_xlim([0, 100])
            ax.set_ylim([0, 1.15])
            ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
            ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
            
            # Add description box
            description = (
                "This chart shows the fuzzy membership functions for the recommendation output.\n"
                "Vertical dashed lines indicate where each recommended movie falls on the scale.\n"
                "Higher scores indicate stronger recommendations based on fuzzy inference."
            )
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
            ax.text(0.5, -0.15, description, transform=ax.transAxes,
                   fontsize=9, va='top', ha='center', bbox=props, wrap=True)
            
            plt.tight_layout()
            
            # Save
            output_path = Path("visualizations") / "membership_functions.png"
            output_path.parent.mkdir(exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(output_path)
            
        except Exception as e:
            print(f"Error plotting membership functions: {e}")
            return None
    
    def _visualize_system_ui(self):
        """Visualize fuzzy logic system."""
        self.ui.clear_screen()
        self.ui.print_section("FUZZY LOGIC VISUALIZATION")
        
        try:
            self.ui.print_info("Generating membership function plots...")
            
            # Membership functions
            mf_path = self.viz.plot_membership_functions(
                self.fuzzy_vars, 
                show=False
            )
            self.ui.print_success(f"Membership functions: {mf_path}")
            
            # Sample inference
            self.ui.print_info("Generating sample inference visualization...")
            
            sample_input = {
                'user_rating': 8.5,
                'actor_popularity': 75.0,
                'genre_match': 85.0
            }
            
            result = self.engine.fuzzy_recommender.recommend_movie(
                sample_input['user_rating'],
                sample_input['actor_popularity'],
                sample_input['genre_match']
            )
            
            inf_path = self.viz.plot_fuzzy_inference(
                sample_input,
                result.recommendation_score,
                self.fuzzy_vars,
                show=False
            )
            self.ui.print_success(f"Inference process: {inf_path}")
            
            # Dashboard
            self.ui.print_info("Creating system dashboard...")
            
            dashboard_path = self.viz.create_dashboard(
                self.fuzzy_vars,
                self.movies_df,
                sample_inference={'inputs': sample_input, 'output': result.recommendation_score},
                show=False
            )
            self.ui.print_success(f"Dashboard: {dashboard_path}")
            
            print()
            self.ui.print_success("All visualizations generated successfully!")
            self.ui.print_info(f"Check the '{self.viz.output_dir}' folder")
            
        except Exception as e:
            self.ui.print_error(f"Visualization error: {e}")
        
        self.ui.wait_for_user()
    
    def _analyze_preferences_ui(self):
        """Analyze user preferences."""
        self.ui.clear_screen()
        self.ui.print_section("USER PREFERENCE ANALYSIS")
        
        genres = self.ui.input_styled("Your favorite genres (comma-separated)", "Action, Sci-Fi")
        genre_list = [g.strip() for g in genres.split(',')]
        
        # Analyze
        analysis = {}
        for genre in genre_list:
            matches = self.movies_df[
                self.movies_df['genres'].str.contains(genre, case=False, na=False)
            ]
            analysis[genre] = {
                'count': len(matches),
                'avg_rating': matches['average_rating'].mean() if len(matches) > 0 else 0
            }
        
        print()
        self.ui.print_section("ANALYSIS RESULTS")
        
        headers = ["Genre", "Movies Available", "Avg Rating"]
        rows = []
        for genre, data in analysis.items():
            rows.append([
                genre,
                str(data['count']),
                f"{data['avg_rating']:.2f}/10"
            ])
        
        self.ui.print_table(headers, rows, "Genre Analysis")
        
        self.ui.wait_for_user()
    
    def _show_dashboard_ui(self):
        """Show system dashboard."""
        self.ui.clear_screen()
        self.ui.print_section("SYSTEM DASHBOARD")
        
        # System stats
        stats = {
            'Total Movies': len(self.movies_df),
            'Average Rating': f"{self.movies_df['average_rating'].mean():.2f}",
            'Rating Range': f"{self.movies_df['average_rating'].min():.1f} - {self.movies_df['average_rating'].max():.1f}",
            'Fuzzy Variables': 4,
            'Membership Functions': 16,
            'Fuzzy Rules': len(self.engine.fuzzy_recommender.rule_engine.rules),
            'Inference Method': 'Mamdani',
            'Defuzzification': 'Centroid'
        }
        
        self.ui.print_key_value(stats)
        
        # Genre distribution
        all_genres = []
        for genres in self.movies_df['genres']:
            if isinstance(genres, str):
                all_genres.extend(genres.split('|'))
        
        genre_counts = pd.Series(all_genres).value_counts().head(8)
        
        print()
        self.ui.print_section("TOP GENRES")
        
        headers = ["Genre", "Count", "Percentage"]
        rows = []
        total = len(all_genres)
        for genre, count in genre_counts.items():
            rows.append([
                genre,
                str(count),
                f"{(count/total*100):.1f}%"
            ])
        
        self.ui.print_table(headers, rows)
        
        self.ui.wait_for_user()
    
    def _explore_database_ui(self):
        """Explore movie database."""
        self.ui.clear_screen()
        self.ui.print_section("MOVIE DATABASE EXPLORER")
        
        options = [
            "Show random movies",
            "Search by genre",
            "Show top rated",
            "View statistics",
            "Back to main menu"
        ]
        
        choice = self.ui.print_menu("EXPLORER OPTIONS", options)
        
        if choice == '1':
            # Random movies
            random_movies = self.movies_df.sample(n=min(5, len(self.movies_df)))
            
            headers = ["Title", "Rating", "Genres", "Year"]
            rows = []
            for _, movie in random_movies.iterrows():
                rows.append([
                    movie['title'][:30],
                    f"{movie['average_rating']:.1f}/10",
                    movie['genres'][:30],
                    str(movie.get('release_year', 'N/A'))
                ])
            
            self.ui.print_table(headers, rows, "Random Movies")
            
        elif choice == '2':
            # Search by genre
            genre = self.ui.input_styled("Enter genre", "Action")
            matches = self.movies_df[
                self.movies_df['genres'].str.contains(genre, case=False, na=False)
            ].head(10)
            
            headers = ["Title", "Rating", "Genres"]
            rows = []
            for _, movie in matches.iterrows():
                rows.append([
                    movie['title'][:35],
                    f"{movie['average_rating']:.1f}/10",
                    movie['genres'][:35]
                ])
            
            self.ui.print_table(headers, rows, f"Movies in '{genre}'")
            
        elif choice == '3':
            # Top rated
            top_movies = self.movies_df.nlargest(10, 'average_rating')
            
            headers = ["Rank", "Title", "Rating", "Genres"]
            rows = []
            for i, (_, movie) in enumerate(top_movies.iterrows(), 1):
                rows.append([
                    str(i),
                    movie['title'][:30],
                    f"{movie['average_rating']:.1f}/10",
                    movie['genres'][:30]
                ])
            
            self.ui.print_table(headers, rows, "Top Rated Movies")
            
        elif choice == '4':
            # Statistics
            self.ui.print_info("Generating data visualization...")
            
            viz_path = self.viz.plot_data_statistics(self.movies_df, show=False)
            self.ui.print_success(f"Statistics visualization: {viz_path}")
        
        self.ui.wait_for_user()
    
    def _test_inference_ui(self):
        """Test fuzzy inference with custom inputs."""
        self.ui.clear_screen()
        self.ui.print_section("FUZZY INFERENCE TESTER")
        
        self.ui.print_info("Enter test values for fuzzy variables:")
        print()
        
        rating = self.ui.input_styled("User Rating (1-10)", "8.0")
        popularity = self.ui.input_styled("Actor Popularity (0-100)", "75")
        match = self.ui.input_styled("Genre Match (0-100)", "85")
        
        try:
            rating = float(rating)
            popularity = float(popularity)
            match = float(match)
            
            # Run inference
            self.ui.print_info("Running fuzzy inference...")
            
            start = time.time()
            result = self.engine.fuzzy_recommender.recommend_movie(
                rating, popularity, match, include_explanation=True
            )
            elapsed = (time.time() - start) * 1000
            
            # Display results
            print()
            self.ui.print_section("INFERENCE RESULTS")
            
            self.ui.print_key_value({
                'User Rating': f"{rating:.1f}",
                'Actor Popularity': f"{popularity:.1f}",
                'Genre Match': f"{match:.1f}",
                '': '',
                'Recommendation Score': f"{result.recommendation_score:.2f}/100",
                'Confidence': f"{result.confidence:.3f}",
                'Processing Time': f"{elapsed:.2f} ms"
            })
            
            # Interpretation
            print()
            if result.recommendation_score >= 80:
                self.ui.print_success("HIGHLY RECOMMENDED - Excellent match!")
            elif result.recommendation_score >= 60:
                self.ui.print_success("RECOMMENDED - Good choice")
            elif result.recommendation_score >= 40:
                self.ui.print_warning("POSSIBLY RECOMMENDED - Might be worth watching")
            else:
                self.ui.print_warning("NOT RECOMMENDED - May not suit preferences")
            
            # Save to history
            self._add_to_history(
                inputs={
                    'user_rating': rating,
                    'actor_popularity': popularity,
                    'genre_match': match
                },
                output=result.recommendation_score
            )
            
            # Generate visualization
            print()
            generate = self.ui.input_styled("Generate visualization? (y/n)", "y")
            
            if generate.lower() == 'y':
                self.ui.print_info("Creating inference visualization...")
                
                viz_path = self.viz.plot_fuzzy_inference(
                    {
                        'user_rating': rating,
                        'actor_popularity': popularity,
                        'genre_match': match
                    },
                    result.recommendation_score,
                    self.fuzzy_vars,
                    show=False
                )
                
                self.ui.print_success(f"Visualization saved: {viz_path}")
            
        except Exception as e:
            self.ui.print_error(f"Error in inference: {e}")
        
        self.ui.wait_for_user()
    
    # ========== NEW FEATURES ==========
    
    def _load_history(self) -> List[Dict]:
        """Load recommendation history from JSON file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _get_available_genres(self) -> List[str]:
        """Get list of all genres available in current dataset."""
        if self.movies_df is None:
            return []
        
        genres_set = set()
        for genres_str in self.movies_df['genres']:
            if pd.notna(genres_str):
                # Split by | or , or ;
                for sep in ['|', ',', ';']:
                    genres_str = genres_str.replace(sep, '|')
                genres = [g.strip() for g in genres_str.split('|')]
                genres_set.update(genres)
        
        return sorted(list(genres_set))
    
    def _get_fuzzy_label(self, score: float) -> Tuple[str, str]:
        """
        Get fuzzy linguistic label and visual indicator for a recommendation score.
        
        Args:
            score: Recommendation score (0-100)
            
        Returns:
            Tuple of (label, visual_indicator)
            - label: Linguistic term
            - visual_indicator: Stars/symbols for display
        """
        import skfuzzy as fuzz
        
        # Get membership degrees for all labels
        universe = np.arange(0, 101, 1)
        
        # Define membership functions (same as in variables.py)
        not_recommended = fuzz.trimf(universe, [0, 0, 25])
        possibly_recommended = fuzz.trimf(universe, [15, 40, 65])
        recommended = fuzz.trimf(universe, [50, 75, 90])
        highly_recommended = fuzz.trimf(universe, [80, 100, 100])
        
        # Calculate membership degrees for current score
        score_idx = min(int(score), 100)
        degrees = {
            'Not Recommended': not_recommended[score_idx],
            'Possibly': possibly_recommended[score_idx],
            'Recommended': recommended[score_idx],
            'Highly Recommended': highly_recommended[score_idx]
        }
        
        # Get label with maximum membership degree
        max_label = max(degrees, key=degrees.get)
        max_degree = degrees[max_label]
        
        # Assign visual indicators based on label
        visual_map = {
            'Highly Recommended': '★★★',
            'Recommended': '★★☆',
            'Possibly': '★☆☆',
            'Not Recommended': '☆☆☆'
        }
        
        visual = visual_map.get(max_label, '---')
        
        return max_label, visual
    
    def _save_history(self):
        """Save recommendation history to JSON file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.recommendation_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.ui.print_error(f"Error saving history: {e}")
    
    def _add_to_history(self, inputs: Dict, output: float, movie_title: str = None):
        """Add recommendation to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'inputs': inputs,
            'output': output,
            'movie': movie_title
        }
        self.recommendation_history.append(entry)
        
        # Keep only last 100 entries
        if len(self.recommendation_history) > 100:
            self.recommendation_history = self.recommendation_history[-100:]
    
    def _add_custom_movie_ui(self):
        """Add custom movie to dataset."""
        self.ui.clear_screen()
        self.ui.print_section("ADD CUSTOM MOVIE")
        
        try:
            # Show available genres
            available_genres = self._get_available_genres()
            if available_genres:
                print()
                self.ui.print_info(f"Available genres ({len(available_genres)}): {', '.join(available_genres[:20])}")
                self.ui.print_info("Tip: Use existing genres for better recommendations")
                print()
            
            # Get movie details
            title = self.ui.input_styled("Movie Title", "The Matrix")
            
            if not title:
                self.ui.print_warning("Title is required")
                self.ui.wait_for_user()
                return
            
            genres = self.ui.input_styled("Genres (comma-separated)", "Action, Sci-Fi")
            actors = self.ui.input_styled("Main Actors (comma-separated)", "Keanu Reeves, Laurence Fishburne")
            rating_str = self.ui.input_styled("Average Rating (1-10)", "8.7")
            year_str = self.ui.input_styled("Release Year", "1999")
            director = self.ui.input_styled("Director", "Wachowski Brothers")
            
            # Validate and convert
            try:
                rating = float(rating_str) if rating_str else 7.0
                rating = max(1.0, min(10.0, rating))
            except:
                rating = 7.0
            
            try:
                year = int(year_str) if year_str else 2000
            except:
                year = 2000
            
            # Create new movie entry
            new_movie = {
                'movie_id': f'custom_{int(time.time())}',
                'title': title,
                'genres': genres if genres else 'Unknown',
                'actors': actors if actors else 'Unknown',  # Use 'actors' to match system standard
                'director': director if director else 'Unknown',
                'average_rating': rating,
                'release_year': year,
                'custom_added': True,
                'added_timestamp': datetime.now().isoformat()
            }
            
            # Add to current dataset
            self.movies_df = pd.concat([
                self.movies_df,
                pd.DataFrame([new_movie])
            ], ignore_index=True)
            
            # Save to custom movies file
            custom_file = self.data_dir / "custom_movies.csv"
            
            if custom_file.exists():
                custom_df = pd.read_csv(custom_file)
                custom_df = pd.concat([custom_df, pd.DataFrame([new_movie])], ignore_index=True)
            else:
                custom_df = pd.DataFrame([new_movie])
            
            custom_df.to_csv(custom_file, index=False)
            
            # Reinitialize engine with new data
            self.engine.load_data(self.movies_df)
            
            print()
            self.ui.print_success(f"Movie '{title}' added successfully!")
            self.ui.print_info(f"Total movies in database: {len(self.movies_df)}")
            self.ui.print_info(f"Custom movies saved to: {custom_file}")
            
            # Debug: Verify integration
            print()
            self.ui.print_info("Verifying integration...")
            custom_in_df = self.movies_df[self.movies_df['title'] == title]
            if len(custom_in_df) > 0:
                self.ui.print_success(f"✓ '{title}' found in memory DataFrame")
            else:
                self.ui.print_warning(f"✗ '{title}' NOT found in memory DataFrame")
            
            # Check engine database size
            if hasattr(self.engine, 'data_preprocessor'):
                engine_size = len(self.engine.data_preprocessor.movie_database)
                self.ui.print_info(f"Engine database size: {engine_size} movies")
                
                # Check if custom movie is in engine
                engine_has_movie = title in self.engine.data_preprocessor.movie_database['title'].values
                if engine_has_movie:
                    self.ui.print_success(f"✓ '{title}' found in engine database")
                else:
                    self.ui.print_warning(f"✗ '{title}' NOT found in engine database")
            
        except Exception as e:
            self.ui.print_error(f"Error adding movie: {e}")
        
        self.ui.wait_for_user()
    
    def _export_dataset_ui(self):
        """Export current dataset in multiple formats."""
        self.ui.clear_screen()
        self.ui.print_section("EXPORT DATASET")
        
        print()
        self.ui.print_info(f"Current dataset: {len(self.movies_df)} movies")
        print()
        
        options = [
            "Export as CSV",
            "Export as JSON",
            "Export as Excel",
            "Export all formats",
            "Back to menu"
        ]
        
        choice = self.ui.print_menu("EXPORT OPTIONS", options)
        
        if choice == '5':
            return
        
        formats = []
        if choice == '1':
            formats = ['csv']
        elif choice == '2':
            formats = ['json']
        elif choice == '3':
            formats = ['excel']
        elif choice == '4':
            formats = ['csv', 'json', 'excel']
        
        if formats:
            self.export_dataset(formats)
        
        self.ui.wait_for_user()
    
    def export_dataset(self, formats):
        """Export dataset in specified formats."""
        if isinstance(formats, str):
            formats = [formats] if formats != 'all' else ['csv', 'json', 'excel']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_dir = self.data_dir / f"export_{timestamp}"
        export_dir.mkdir(exist_ok=True)
        
        exported_files = []
        
        try:
            for fmt in formats:
                if fmt == 'csv':
                    filepath = export_dir / "movies_export.csv"
                    self.movies_df.to_csv(filepath, index=False)
                    exported_files.append(str(filepath))
                    
                elif fmt == 'json':
                    filepath = export_dir / "movies_export.json"
                    self.movies_df.to_json(filepath, orient='records', indent=2)
                    exported_files.append(str(filepath))
                    
                elif fmt == 'excel':
                    filepath = export_dir / "movies_export.xlsx"
                    try:
                        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                            self.movies_df.to_excel(writer, sheet_name='Movies', index=False)
                            
                            # Add statistics sheet
                            stats_data = {
                                'Metric': [
                                    'Total Movies',
                                    'Average Rating',
                                    'Highest Rating',
                                    'Lowest Rating',
                                    'Unique Genres',
                                    'Export Date'
                                ],
                                'Value': [
                                    len(self.movies_df),
                                    f"{self.movies_df['average_rating'].mean():.2f}",
                                    f"{self.movies_df['average_rating'].max():.2f}",
                                    f"{self.movies_df['average_rating'].min():.2f}",
                                    len(set(g for genres in self.movies_df['genres'] for g in str(genres).split('|'))),
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                ]
                            }
                            stats_df = pd.DataFrame(stats_data)
                            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                        
                        exported_files.append(str(filepath))
                    except Exception as e:
                        self.ui.print_warning(f"Excel export failed: {e}")
            
            print()
            self.ui.print_success(f"Dataset exported successfully to: {export_dir}")
            for filepath in exported_files:
                self.ui.print_info(f"  {Path(filepath).name}")
                
        except Exception as e:
            self.ui.print_error(f"Export error: {e}")
    
    def _view_history_ui(self):
        """View recommendation history."""
        self.ui.clear_screen()
        self.ui.print_section("RECOMMENDATION HISTORY")
        
        if not self.recommendation_history:
            print()
            self.ui.print_warning("No recommendations in history yet")
            self.ui.wait_for_user()
            return
        
        print()
        self.ui.print_info(f"Total recommendations: {len(self.recommendation_history)}")
        print()
        
        # Show last 10 recommendations
        recent = self.recommendation_history[-10:]
        
        headers = ["#", "Date/Time", "Rating", "Popularity", "Genre", "Score", "Movie"]
        rows = []
        
        for i, entry in enumerate(reversed(recent), 1):
            dt = datetime.fromisoformat(entry['timestamp'])
            date_str = dt.strftime('%m/%d %H:%M')
            
            inputs = entry['inputs']
            rows.append([
                str(i),
                date_str,
                f"{inputs.get('user_rating', 'N/A')}",
                f"{inputs.get('actor_popularity', 'N/A')}",
                f"{inputs.get('genre_match', 'N/A')}",
                f"{entry['output']:.1f}",
                entry.get('movie', 'N/A')[:20]
            ])
        
        self.ui.print_table(headers, rows, "Last 10 Recommendations")
        
        print()
        export = self.ui.input_styled("Export full history? (y/n)", "n")
        
        if export.lower() == 'y':
            export_file = self.data_dir / f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(self.recommendation_history, f, indent=2, ensure_ascii=False)
                self.ui.print_success(f"History exported to: {export_file}")
            except Exception as e:
                self.ui.print_error(f"Export failed: {e}")
        
        self.ui.wait_for_user()
    
    def _generate_sample_dataset_ui(self):
        """Generate sample dataset interactively."""
        self.ui.clear_screen()
        self.ui.print_section("GENERATE SAMPLE DATASET")
        
        print()
        num_str = self.ui.input_styled("Number of movies to generate", "100")
        
        try:
            num_movies = int(num_str)
            num_movies = max(10, min(1000, num_movies))  # Limit 10-1000
        except:
            num_movies = 100
        
        self.generate_sample_data(num_movies)
        self.ui.wait_for_user()
    
    def generate_sample_data(self, num_movies: int):
        """Generate sample dataset in multiple formats."""
        self.ui.clear_screen()
        self.ui.print_section("SAMPLE DATA GENERATOR")
        
        print()
        self.ui.print_info(f"Generating {num_movies} sample movies...")
        
        try:
            # Generate data
            data_loader = EnhancedDataLoader(enable_caching=False)
            sample_data = data_loader.create_sample_dataset(num_movies=num_movies)
            
            # Create output directory
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = self.generated_data_dir / f"dataset_{timestamp}"
            output_dir.mkdir(exist_ok=True)
            
            # Save in multiple formats
            files_created = []
            
            # CSV
            csv_path = output_dir / "sample_movies.csv"
            sample_data.to_csv(csv_path, index=False)
            files_created.append(csv_path)
            
            # JSON
            json_path = output_dir / "sample_movies.json"
            sample_data.to_json(json_path, orient='records', indent=2)
            files_created.append(json_path)
            
            # Excel with statistics
            try:
                excel_path = output_dir / "sample_movies.xlsx"
                with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                    sample_data.to_excel(writer, sheet_name='Movies', index=False)
                    
                    # Statistics
                    all_genres = []
                    for genres in sample_data['genres'].dropna():
                        all_genres.extend(str(genres).split('|'))
                    genre_counts = pd.Series(all_genres).value_counts().head(10)
                    
                    stats_data = {
                        'Total Movies': [len(sample_data)],
                        'Average Rating': [f"{sample_data['average_rating'].mean():.2f}"],
                        'Rating Std Dev': [f"{sample_data['average_rating'].std():.2f}"],
                        'Min Rating': [f"{sample_data['average_rating'].min():.2f}"],
                        'Max Rating': [f"{sample_data['average_rating'].max():.2f}"],
                        'Unique Genres': [len(set(all_genres))],
                        'Most Common Genre': [genre_counts.index[0] if len(genre_counts) > 0 else 'N/A'],
                        'Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                    }
                    stats_df = pd.DataFrame(stats_data).T.reset_index()
                    stats_df.columns = ['Metric', 'Value']
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                    
                    # Genre distribution
                    genre_df = pd.DataFrame({
                        'Genre': genre_counts.index,
                        'Count': genre_counts.values
                    })
                    genre_df.to_excel(writer, sheet_name='Genre Distribution', index=False)
                
                files_created.append(excel_path)
            except Exception as e:
                self.ui.print_warning(f"Excel export skipped: {e}")
            
            # Create README
            readme_path = output_dir / "README.txt"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"Sample Movie Dataset\n")
                f.write(f"={'='*50}\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Movies: {len(sample_data)}\n")
                f.write(f"Average Rating: {sample_data['average_rating'].mean():.2f}\n")
                f.write(f"Rating Range: {sample_data['average_rating'].min():.1f} - {sample_data['average_rating'].max():.1f}\n\n")
                f.write(f"Files:\n")
                for file in files_created:
                    f.write(f"  - {file.name}\n")
                f.write(f"\nTop Genres:\n")
                for genre, count in genre_counts.head(5).items():
                    f.write(f"  {genre}: {count} movies\n")
            
            # Display results
            print()
            self.ui.print_success(f"Dataset generated successfully!")
            print()
            self.ui.print_key_value({
                'Output Directory': str(output_dir),
                'Total Movies': len(sample_data),
                'Average Rating': f"{sample_data['average_rating'].mean():.2f}",
                'Files Created': len(files_created)
            })
            
            print()
            self.ui.print_section("FILES CREATED")
            for filepath in files_created:
                self.ui.print_info(f"  {filepath.name}")
            
            print()
            self.ui.print_section("TOP 5 GENRES")
            for genre, count in genre_counts.head(5).items():
                print(f"  {genre}: {count} movies")
            
        except Exception as e:
            self.ui.print_error(f"Error generating data: {e}")
            import traceback
            traceback.print_exc()
    
    def _manage_datasets_ui(self):
        """Manage datasets (load, switch, delete)."""
        self.ui.clear_screen()
        self.ui.print_section("DATASET MANAGER")
        
        print()
        
        options = [
            "Load custom CSV dataset",
            "View available datasets",
            "Reload current dataset",
            "Show dataset info",
            "Back to menu"
        ]
        
        choice = self.ui.print_menu("DATASET OPTIONS", options)
        
        if choice == '1':
            self._load_custom_dataset()
        elif choice == '2':
            self._list_available_datasets()
        elif choice == '3':
            self.initialize_system(num_movies=len(self.movies_df), verbose=True)
            self.ui.print_success("Dataset reloaded")
        elif choice == '4':
            self._show_dataset_info()
        
        if choice != '5':
            self.ui.wait_for_user()
    
    def _load_custom_dataset(self):
        """Load a custom CSV dataset."""
        print()
        filepath = self.ui.input_styled("CSV file path", "data/custom_movies.csv")
        
        try:
            custom_df = pd.read_csv(filepath)
            
            # Validate required columns
            required_cols = ['title', 'average_rating']
            missing = [col for col in required_cols if col not in custom_df.columns]
            
            if missing:
                self.ui.print_error(f"Missing required columns: {', '.join(missing)}")
                return
            
            self.movies_df = custom_df
            self.engine.load_data(self.movies_df)
            
            print()
            self.ui.print_success(f"Loaded {len(custom_df)} movies from {filepath}")
            
        except Exception as e:
            self.ui.print_error(f"Error loading dataset: {e}")
    
    def _list_available_datasets(self):
        """List available datasets in data/ and generated_data/."""
        print()
        self.ui.print_info("Searching for datasets...")
        
        datasets = []
        
        # Search in data/
        for csv_file in self.data_dir.glob("*.csv"):
            datasets.append(('data', csv_file))
        
        # Search in generated_data/
        for subdir in self.generated_data_dir.iterdir():
            if subdir.is_dir():
                for csv_file in subdir.glob("*.csv"):
                    datasets.append(('generated', csv_file))
        
        if not datasets:
            self.ui.print_warning("No datasets found")
            return
        
        print()
        headers = ["#", "Type", "Filename", "Size", "Modified"]
        rows = []
        
        for i, (dtype, filepath) in enumerate(datasets, 1):
            stat = filepath.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            size_kb = stat.st_size / 1024
            
            rows.append([
                str(i),
                dtype.title(),
                filepath.name,
                f"{size_kb:.1f} KB",
                mod_time
            ])
        
        self.ui.print_table(headers, rows, f"Available Datasets ({len(datasets)})")
    
    def _show_dataset_info(self):
        """Show information about current dataset."""
        print()
        self.ui.print_section("CURRENT DATASET INFO")
        
        info = {
            'Total Movies': len(self.movies_df),
            'Columns': ', '.join(self.movies_df.columns[:5]) + '...',
            'Memory Usage': f"{self.movies_df.memory_usage(deep=True).sum() / 1024:.1f} KB",
            'Average Rating': f"{self.movies_df['average_rating'].mean():.2f}",
            'Rating Std Dev': f"{self.movies_df['average_rating'].std():.2f}",
            'Duplicates': self.movies_df.duplicated().sum()
        }
        
        self.ui.print_key_value(info)
    
    def _view_dataset_info_ui(self):
        """View comprehensive dataset information."""
        self.ui.clear_screen()
        self.ui.print_section("DATASET INFORMATION")
        
        # Basic stats
        print()
        self.ui.print_info("=== GENERAL STATISTICS ===")
        print()
        
        total_movies = len(self.movies_df)
        custom_movies = len(self.movies_df[self.movies_df.get('custom_added', False) == True]) if 'custom_added' in self.movies_df.columns else 0
        generated_movies = total_movies - custom_movies
        
        basic_info = {
            'Total Movies': total_movies,
            'Generated Movies': generated_movies,
            'Custom Movies': custom_movies,
            'Memory Usage': f"{self.movies_df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        }
        
        self.ui.print_key_value(basic_info)
        
        # Rating stats
        print()
        self.ui.print_info("=== RATING STATISTICS ===")
        print()
        
        rating_stats = {
            'Average Rating': f"{self.movies_df['average_rating'].mean():.2f}",
            'Min Rating': f"{self.movies_df['average_rating'].min():.2f}",
            'Max Rating': f"{self.movies_df['average_rating'].max():.2f}",
            'Std Deviation': f"{self.movies_df['average_rating'].std():.2f}"
        }
        
        self.ui.print_key_value(rating_stats)
        
        # Available genres
        print()
        self.ui.print_info("=== AVAILABLE GENRES ===")
        print()
        
        genres_list = self._get_available_genres()
        print(f"Total genres: {len(genres_list)}")
        print()
        
        # Display genres in columns
        cols = 4
        for i in range(0, len(genres_list), cols):
            row_genres = genres_list[i:i+cols]
            print("  ".join(f"{g:<20}" for g in row_genres))
        
        # Custom movies list
        if custom_movies > 0:
            print()
            print()
            self.ui.print_info(f"=== CUSTOM MOVIES ({custom_movies}) ===")
            print()
            
            custom_df = self.movies_df[self.movies_df.get('custom_added', False) == True]
            headers = ["Title", "Genres", "Rating", "Year"]
            rows = []
            
            for _, movie in custom_df.head(10).iterrows():
                rows.append([
                    movie['title'][:30],
                    movie.get('genres', 'N/A')[:25],
                    f"{movie.get('average_rating', 0):.1f}",
                    str(movie.get('release_year', 'N/A'))
                ])
            
            self.ui.print_table(headers, rows, f"Custom Movies (showing {min(10, custom_movies)} of {custom_movies})")
        
        self.ui.wait_for_user()
    
    def run_batch_tests(self):
        """Run comprehensive batch testing."""
        self.ui.clear_screen()
        self.ui.print_header("BATCH TESTING SUITE", "Comprehensive System Validation")
        
        if not self.initialize_system(num_movies=100, verbose=True):
            return
        
        print()
        self.ui.print_section("TEST 1: PERFORMANCE TESTING")
        
        # Performance test
        test_cases = [
            (3.0, 25.0, 30.0),
            (5.0, 50.0, 50.0),
            (7.0, 70.0, 70.0),
            (9.0, 90.0, 90.0)
        ]
        
        times = []
        for rating, pop, match in test_cases:
            start = time.time()
            result = self.engine.fuzzy_recommender.recommend_movie(rating, pop, match)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        headers = ["Metric", "Value"]
        rows = [
            ["Average Time", f"{np.mean(times):.2f} ms"],
            ["Min Time", f"{np.min(times):.2f} ms"],
            ["Max Time", f"{np.max(times):.2f} ms"],
            ["Std Dev", f"{np.std(times):.2f} ms"]
        ]
        
        self.ui.print_table(headers, rows, "Performance Results")
        
        # Accuracy test
        print()
        print()
        self.ui.print_section("TEST 2: ACCURACY TESTING")
        
        expected_ranges = [
            ((3.0, 25.0, 30.0), (0, 40), "Low inputs should give low scores"),
            ((9.0, 90.0, 90.0), (70, 100), "High inputs should give high scores"),
            ((5.0, 50.0, 50.0), (35, 65), "Medium inputs should give medium scores")
        ]
        
        accuracy_results = []
        for inputs, (min_exp, max_exp), desc in expected_ranges:
            result = self.engine.fuzzy_recommender.recommend_movie(*inputs)
            score = result.recommendation_score
            passed = min_exp <= score <= max_exp
            accuracy_results.append([
                desc,
                f"{score:.1f}",
                f"{min_exp}-{max_exp}",
                "[OK]" if passed else "[FAIL]"
            ])
        
        headers = ["Test Case", "Actual", "Expected", "Result"]
        self.ui.print_table(headers, accuracy_results, "Accuracy Results")
        
        # Robustness test
        print()
        print()
        self.ui.print_section("TEST 3: ROBUSTNESS TESTING")
        
        edge_cases = [
            ((1.0, 0.0, 0.0), "Minimum values"),
            ((10.0, 100.0, 100.0), "Maximum values"),
            ((5.5, 55.5, 55.5), "Decimal values"),
            ((1.0, 100.0, 0.0), "Mixed extremes")
        ]
        
        robustness_results = []
        for inputs, desc in edge_cases:
            try:
                result = self.engine.fuzzy_recommender.recommend_movie(*inputs)
                status = "[OK]"
                score = f"{result.recommendation_score:.1f}"
            except Exception as e:
                status = "[FAIL]"
                score = f"Error: {str(e)[:20]}"
            
            robustness_results.append([
                desc,
                f"{inputs[0]}, {inputs[1]}, {inputs[2]}",
                score,
                status
            ])
        
        headers = ["Test Case", "Inputs", "Output", "Status"]
        self.ui.print_table(headers, robustness_results, "Robustness Results")
        
        print()
        print()
        self.ui.print_success("BATCH TESTING COMPLETED!")
        self.ui.print_info("All tests executed successfully")
        
        self.ui.wait_for_user()
    
    # ========== END NEW FEATURES ==========
    
    def run_demo_mode(self):
        """Run demonstration mode."""
        self.ui.clear_screen()
        self.ui.print_header("FUZZY LOGIC SYSTEM DEMONSTRATION",
                            "Comprehensive System Overview")
        
        if not self.initialize_system(num_movies=50, verbose=False):
            return
        
        # 1. System Overview
        self.ui.print_section("SYSTEM ARCHITECTURE")
        
        architecture = {
            'Fuzzy Variables': '4 (User Rating, Actor Popularity, Genre Match, Recommendation)',
            'Membership Functions': '16 (Triangular & Trapezoidal)',
            'Fuzzy Rules': f'{len(self.engine.fuzzy_recommender.rule_engine.rules)} comprehensive rules',
            'Inference Method': 'Mamdani',
            'Defuzzification': 'Centroid method',
            'Dataset': f'{len(self.movies_df)} movies loaded'
        }
        
        self.ui.print_key_value(architecture)
        
        # 2. Sample Inference
        print()
        self.ui.print_section("SAMPLE FUZZY INFERENCE")
        
        test_cases = [
            {'rating': 3.0, 'pop': 25.0, 'match': 30.0, 'desc': 'Low values'},
            {'rating': 6.5, 'pop': 60.0, 'match': 70.0, 'desc': 'Medium values'},
            {'rating': 9.0, 'pop': 85.0, 'match': 95.0, 'desc': 'High values'}
        ]
        
        headers = ["Test Case", "User Rating", "Actor Pop", "Genre Match", "Output Score", "Result"]
        rows = []
        
        for case in test_cases:
            result = self.engine.fuzzy_recommender.recommend_movie(
                case['rating'], case['pop'], case['match']
            )
            
            interpretation = "Highly Recommended" if result.recommendation_score >= 80 else \
                           "Recommended" if result.recommendation_score >= 60 else \
                           "Maybe" if result.recommendation_score >= 40 else "Not Recommended"
            
            rows.append([
                case['desc'],
                f"{case['rating']:.1f}",
                f"{case['pop']:.1f}",
                f"{case['match']:.1f}",
                f"{result.recommendation_score:.2f}",
                interpretation
            ])
        
        self.ui.print_table(headers, rows, "Inference Test Results")
        
        # 3. Generate visualizations
        print()
        self.ui.print_section("GENERATING VISUALIZATIONS")
        
        self.ui.print_info("Creating membership functions plot...")
        mf_path = self.viz.plot_membership_functions(self.fuzzy_vars, show=False)
        self.ui.print_success(f"Created: {mf_path}")
        
        self.ui.print_info("Creating system dashboard...")
        dashboard_path = self.viz.create_dashboard(
            self.fuzzy_vars,
            self.movies_df,
            sample_inference={
                'inputs': {'user_rating': 8.5, 'actor_popularity': 75.0, 'genre_match': 85.0},
                'output': 78.5
            },
            show=False
        )
        self.ui.print_success(f"Created: {dashboard_path}")
        
        self.ui.print_info("Creating data statistics...")
        stats_path = self.viz.plot_data_statistics(self.movies_df, show=False)
        self.ui.print_success(f"Created: {stats_path}")
        
        # 4. Sample recommendations
        print()
        self.ui.print_section("SAMPLE RECOMMENDATIONS")
        
        profiles = [
            {'name': 'Action Fan', 'genres': ['Action', 'Thriller'], 'rating': 7.0},
            {'name': 'Drama Lover', 'genres': ['Drama', 'Romance'], 'rating': 8.0},
        ]
        
        for profile in profiles:
            print()
            self.ui.print_info(f"Profile: {profile['name']}")
            
            recs = self.engine.get_recommendations(
                user_preferences={
                    'preferred_genres': profile['genres'],
                    'favorite_actors': [],
                    'min_rating': profile['rating']
                },
                num_recommendations=3
            )
            
            for i, (movie, score, _) in enumerate(recs, 1):
                print(f"  {i}. {movie['title'][:40]} - Score: {score:.1f}/100")
        
        # Summary
        print()
        print()
        self.ui.print_success("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        self.ui.print_info(f"All visualizations saved to '{self.viz.output_dir}' folder")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fuzzy Logic Movie Recommendation System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run demonstration mode')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate all visualizations')
    parser.add_argument('--generate-data', type=int, metavar='N',
                       help='Generate N sample movies in multiple formats (CSV, JSON, Excel)')
    parser.add_argument('--batch-test', action='store_true',
                       help='Run comprehensive batch testing (performance, accuracy, robustness)')
    parser.add_argument('--export', type=str, metavar='FORMAT',
                       choices=['csv', 'json', 'excel', 'all'],
                       help='Export current dataset in specified format')
    
    args = parser.parse_args()
    
    try:
        app = ModernFuzzyApp()
        
        if args.generate_data:
            app.generate_sample_data(args.generate_data)
        elif args.batch_test:
            app.run_batch_tests()
        elif args.export:
            if app.initialize_system(verbose=True):
                app.export_dataset(args.export)
        elif args.demo:
            app.run_demo_mode()
        elif args.visualize:
            app.ui.clear_screen()
            app.ui.print_header("VISUALIZATION GENERATOR")
            if app.initialize_system(verbose=True):
                app._visualize_system_ui()
        else:
            app.run_interactive_mode()
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
