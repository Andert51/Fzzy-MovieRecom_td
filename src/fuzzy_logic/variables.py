"""
Fuzzy Variables Module for Movie Recommendation System

This module defines all the fuzzy variables (antecedents and consequents) used in the 
movie recommendation system. Each variable represents a linguistic concept with 
associated membership functions.

Key Components:
- User Rating: How much a user rates movies (1-10 scale)
- Actor Popularity: Fame level of actors (unknown, known, famous)
- Genre Preference: User's preference for movie genres
- Recommendation Score: Final recommendation strength (0-100 scale)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzyVariables:
    """
    Central class for managing all fuzzy variables in the movie recommendation system.
    
    This class implements the core fuzzy logic components including:
    - Antecedent variables (inputs): user_rating, actor_popularity, genre_match
    - Consequent variable (output): recommendation_score
    
    Each variable uses carefully designed membership functions to capture
    the subjective nature of movie preferences.
    """
    
    def __init__(self):
        """Initialize all fuzzy variables with their membership functions."""
        self._create_input_variables()
        self._create_output_variables()
        
    def _create_input_variables(self):
        """
        Create and configure all input (antecedent) fuzzy variables.
        
        Input Variables:
        1. User Rating (1-10): User's historical rating patterns
        2. Actor Popularity (0-100): Fame/recognition level of main actors
        3. Genre Match (0-100): How well movie genre matches user preferences
        """
        
        # User Rating Variable (1-10 scale)
        # Represents how users typically rate movies they watch
        self.user_rating = ctrl.Antecedent(np.arange(1, 11, 0.1), 'user_rating')
        
        # Define membership functions for user rating using triangular functions
        # These capture different rating behaviors: harsh critics, average users, generous raters
        self.user_rating['low'] = fuzz.trimf(self.user_rating.universe, [1, 1, 4])
        self.user_rating['medium'] = fuzz.trimf(self.user_rating.universe, [2, 5.5, 8])
        self.user_rating['high'] = fuzz.trimf(self.user_rating.universe, [6, 10, 10])
        
        # Actor Popularity Variable (0-100 scale)
        # Represents the fame/recognition level of the main actors
        self.actor_popularity = ctrl.Antecedent(np.arange(0, 101, 1), 'actor_popularity')
        
        # Membership functions for actor popularity using trapezoidal functions
        # These provide smooth transitions between popularity levels
        self.actor_popularity['unknown'] = fuzz.trapmf(self.actor_popularity.universe, [0, 0, 20, 40])
        self.actor_popularity['known'] = fuzz.trapmf(self.actor_popularity.universe, [20, 40, 60, 80])
        self.actor_popularity['famous'] = fuzz.trapmf(self.actor_popularity.universe, [60, 80, 100, 100])
        
        # Genre Match Variable (0-100 scale)
        # Represents how well the movie's genre aligns with user preferences
        self.genre_match = ctrl.Antecedent(np.arange(0, 101, 1), 'genre_match')
        
        # Membership functions for genre matching using triangular functions
        # These capture the degree of genre preference alignment
        self.genre_match['poor'] = fuzz.trimf(self.genre_match.universe, [0, 0, 35])
        self.genre_match['moderate'] = fuzz.trimf(self.genre_match.universe, [20, 50, 80])
        self.genre_match['excellent'] = fuzz.trimf(self.genre_match.universe, [65, 100, 100])
        
    def _create_output_variables(self):
        """
        Create and configure the output (consequent) fuzzy variable.
        
        Output Variable:
        Recommendation Score (0-100): Final recommendation strength
        """
        
        # Recommendation Score Variable (0-100 scale)
        # Represents the final recommendation strength for a movie
        self.recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'recommendation')
        
        # Membership functions for recommendation score using overlapping triangular functions
        # These provide nuanced recommendation levels beyond simple binary choices
        self.recommendation['not_recommended'] = fuzz.trimf(self.recommendation.universe, [0, 0, 25])
        self.recommendation['possibly_recommended'] = fuzz.trimf(self.recommendation.universe, [15, 40, 65])
        self.recommendation['recommended'] = fuzz.trimf(self.recommendation.universe, [50, 75, 90])
        self.recommendation['highly_recommended'] = fuzz.trimf(self.recommendation.universe, [80, 100, 100])
        
    def get_variables(self):
        """
        Return all fuzzy variables for use in rule creation.
        
        Returns:
            dict: Dictionary containing all fuzzy variables
                - user_rating: User rating patterns
                - actor_popularity: Actor fame level
                - genre_match: Genre preference alignment
                - recommendation: Final recommendation score
        """
        return {
            'user_rating': self.user_rating,
            'actor_popularity': self.actor_popularity,
            'genre_match': self.genre_match,
            'recommendation': self.recommendation
        }
    
    def visualize_variables(self, save_plots=False):
        """
        Generate visualization plots for all fuzzy variables and their membership functions.
        
        This method creates comprehensive plots showing:
        - Membership function shapes
        - Linguistic term overlaps
        - Universe of discourse for each variable
        
        Args:
            save_plots (bool): Whether to save plots to files
        """
        
        # Create subplots for all variables
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Fuzzy Variables Membership Functions', fontsize=16, fontweight='bold')
        
        # Plot User Rating membership functions
        axes[0, 0].set_title('User Rating Variable (1-10 scale)', fontweight='bold')
        for label in self.user_rating.terms:
            axes[0, 0].plot(self.user_rating.universe, 
                          self.user_rating[label].mf, 
                          linewidth=2, label=label)
        axes[0, 0].set_xlabel('Rating Value')
        axes[0, 0].set_ylabel('Membership Degree')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot Actor Popularity membership functions
        axes[0, 1].set_title('Actor Popularity Variable (0-100 scale)', fontweight='bold')
        for label in self.actor_popularity.terms:
            axes[0, 1].plot(self.actor_popularity.universe, 
                          self.actor_popularity[label].mf, 
                          linewidth=2, label=label)
        axes[0, 1].set_xlabel('Popularity Score')
        axes[0, 1].set_ylabel('Membership Degree')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot Genre Match membership functions
        axes[1, 0].set_title('Genre Match Variable (0-100 scale)', fontweight='bold')
        for label in self.genre_match.terms:
            axes[1, 0].plot(self.genre_match.universe, 
                          self.genre_match[label].mf, 
                          linewidth=2, label=label)
        axes[1, 0].set_xlabel('Genre Match Score')
        axes[1, 0].set_ylabel('Membership Degree')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot Recommendation Score membership functions
        axes[1, 1].set_title('Recommendation Score Variable (0-100 scale)', fontweight='bold')
        for label in self.recommendation.terms:
            axes[1, 1].plot(self.recommendation.universe, 
                          self.recommendation[label].mf, 
                          linewidth=2, label=label)
        axes[1, 1].set_xlabel('Recommendation Score')
        axes[1, 1].set_ylabel('Membership Degree')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('fuzzy_variables_visualization.png', dpi=300, bbox_inches='tight')
            print("Fuzzy variables visualization saved as 'fuzzy_variables_visualization.png'")
        
        plt.show()
        
    def print_variable_info(self):
        """
        Print detailed information about all fuzzy variables and their characteristics.
        
        This method provides a comprehensive overview of:
        - Variable universes of discourse
        - Linguistic terms for each variable
        - Membership function types and parameters
        """
        
        print("="*80)
        print("FUZZY VARIABLES INFORMATION")
        print("="*80)
        
        variables_info = [
            {
                'name': 'User Rating',
                'variable': self.user_rating,
                'description': 'Represents user rating patterns (1-10 scale)',
                'terms': ['low (harsh critics)', 'medium (average users)', 'high (generous raters)']
            },
            {
                'name': 'Actor Popularity',
                'variable': self.actor_popularity,
                'description': 'Represents actor fame/recognition level (0-100 scale)',
                'terms': ['unknown (indie/new actors)', 'known (established actors)', 'famous (A-list celebrities)']
            },
            {
                'name': 'Genre Match',
                'variable': self.genre_match,
                'description': 'Represents genre preference alignment (0-100 scale)',
                'terms': ['poor (mismatched genres)', 'moderate (somewhat matching)', 'excellent (perfect match)']
            },
            {
                'name': 'Recommendation Score',
                'variable': self.recommendation,
                'description': 'Final recommendation strength (0-100 scale)',
                'terms': ['not_recommended', 'possibly_recommended', 'recommended', 'highly_recommended']
            }
        ]
        
        for var_info in variables_info:
            print(f"\n{var_info['name']}:")
            print(f"  Description: {var_info['description']}")
            print(f"  Universe: [{var_info['variable'].universe.min():.1f}, {var_info['variable'].universe.max():.1f}]")
            print(f"  Linguistic Terms: {', '.join(var_info['terms'])}")
            print(f"  Number of Terms: {len(var_info['variable'].terms)}")
            
        print("\n" + "="*80)


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of fuzzy variables creation and visualization.
    This section shows how to instantiate and use the FuzzyVariables class.
    """
    
    print("Initializing Fuzzy Variables for Movie Recommendation System")
    print("-" * 60)
    
    # Create fuzzy variables instance
    fuzzy_vars = FuzzyVariables()
    
    # Print detailed information about variables
    fuzzy_vars.print_variable_info()
    
    # Get variables dictionary for external use
    variables = fuzzy_vars.get_variables()
    print(f"\nCreated {len(variables)} fuzzy variables:")
    for var_name in variables:
        print(f"  - {var_name}")
    
    # Demonstrate membership degree calculation
    print("\nExample Membership Degree Calculations:")
    print("-" * 40)
    
    # Test user rating membership
    test_rating = 7.5
    rating_memberships = {}
    for term in fuzzy_vars.user_rating.terms:
        membership = fuzz.interp_membership(
            fuzzy_vars.user_rating.universe,
            fuzzy_vars.user_rating[term].mf,
            test_rating
        )
        rating_memberships[term] = membership
        print(f"Rating {test_rating} -> {term}: {membership:.3f}")
    
    # Visualize the variables (uncomment to show plots)
    # fuzzy_vars.visualize_variables(save_plots=True)
