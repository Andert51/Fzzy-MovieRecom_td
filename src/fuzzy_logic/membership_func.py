"""
Membership Functions Module for Fuzzy Logic Movie Recommendation System

This module provides advanced membership function utilities and custom implementations
for the movie recommendation system. It extends the basic fuzzy logic capabilities
with specialized functions for handling movie recommendation scenarios.

Key Features:
- Custom membership function generators
- Advanced membership function shapes (Gaussian, Sigmoidal, etc.)
- Adaptive membership functions that can be tuned based on user behavior
- Utility functions for membership degree calculations
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Union
import warnings

# Suppress numpy warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)


class MembershipFunctions:
    """
    Advanced membership function utilities for fuzzy logic operations.
    
    This class provides both standard and custom membership functions
    specifically designed for movie recommendation scenarios. It includes
    functions for creating, modifying, and analyzing membership functions.
    """
    
    @staticmethod
    def triangular_mf(x: np.ndarray, params: Tuple[float, float, float]) -> np.ndarray:
        """
        Generate triangular membership function.
        
        Triangular membership functions are ideal for representing 
        crisp boundaries with smooth transitions.
        
        Args:
            x (np.ndarray): Universe of discourse
            params (Tuple[float, float, float]): (a, b, c) where:
                - a: left base point
                - b: peak point  
                - c: right base point
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        a, b, c = params
        
        # Validate parameters
        if not (a <= b <= c):
            raise ValueError(f"Invalid triangular parameters: a={a}, b={b}, c={c}. Must satisfy a <= b <= c")
        
        # Calculate membership degrees
        mf = np.zeros_like(x, dtype=float)
        
        # Left slope (a to b)
        left_mask = (x >= a) & (x <= b)
        if b != a:  # Avoid division by zero
            mf[left_mask] = (x[left_mask] - a) / (b - a)
        
        # Right slope (b to c)  
        right_mask = (x > b) & (x <= c)
        if c != b:  # Avoid division by zero
            mf[right_mask] = (c - x[right_mask]) / (c - b)
        
        # Peak handling
        peak_mask = (x == b)
        mf[peak_mask] = 1.0
        
        return mf
    
    @staticmethod
    def trapezoidal_mf(x: np.ndarray, params: Tuple[float, float, float, float]) -> np.ndarray:
        """
        Generate trapezoidal membership function.
        
        Trapezoidal functions are perfect for representing concepts
        with a stable core region and gradual transitions.
        
        Args:
            x (np.ndarray): Universe of discourse
            params (Tuple[float, float, float, float]): (a, b, c, d) where:
                - a: left base point
                - b: left top point
                - c: right top point  
                - d: right base point
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        a, b, c, d = params
        
        # Validate parameters
        if not (a <= b <= c <= d):
            raise ValueError(f"Invalid trapezoidal parameters: a={a}, b={b}, c={c}, d={d}. Must satisfy a <= b <= c <= d")
        
        # Calculate membership degrees
        mf = np.zeros_like(x, dtype=float)
        
        # Left slope (a to b)
        left_mask = (x >= a) & (x <= b)
        if b != a:
            mf[left_mask] = (x[left_mask] - a) / (b - a)
        
        # Flat top (b to c)
        top_mask = (x > b) & (x <= c)
        mf[top_mask] = 1.0
        
        # Right slope (c to d)
        right_mask = (x > c) & (x <= d)
        if d != c:
            mf[right_mask] = (d - x[right_mask]) / (d - c)
        
        # Handle edge cases
        if b == a:  # Left vertical edge
            mf[x == a] = 1.0
        if c == d:  # Right vertical edge
            mf[x == d] = 1.0
            
        return mf
    
    @staticmethod
    def gaussian_mf(x: np.ndarray, params: Tuple[float, float]) -> np.ndarray:
        """
        Generate Gaussian (bell-shaped) membership function.
        
        Gaussian functions provide smooth, symmetric membership
        distributions ideal for continuous variables.
        
        Args:
            x (np.ndarray): Universe of discourse
            params (Tuple[float, float]): (mean, sigma) where:
                - mean: center of the bell curve
                - sigma: standard deviation (controls width)
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        mean, sigma = params
        
        if sigma <= 0:
            raise ValueError(f"Sigma must be positive, got: {sigma}")
        
        # Calculate Gaussian membership function
        mf = np.exp(-0.5 * ((x - mean) / sigma) ** 2)
        
        return mf
    
    @staticmethod
    def sigmoidal_mf(x: np.ndarray, params: Tuple[float, float]) -> np.ndarray:
        """
        Generate sigmoidal membership function.
        
        Sigmoidal functions are excellent for representing
        monotonic increases or decreases in membership.
        
        Args:
            x (np.ndarray): Universe of discourse
            params (Tuple[float, float]): (a, c) where:
                - a: slope factor (positive for increasing, negative for decreasing)
                - c: crossover point (where membership = 0.5)
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        a, c = params
        
        if a == 0:
            raise ValueError("Slope parameter 'a' cannot be zero")
        
        # Calculate sigmoidal membership function
        # Using stable computation to avoid overflow
        z = a * (x - c)
        
        # Clip extreme values to prevent overflow
        z = np.clip(z, -500, 500)
        
        mf = 1.0 / (1.0 + np.exp(-z))
        
        return mf
    
    @staticmethod
    def pi_shaped_mf(x: np.ndarray, params: Tuple[float, float, float, float]) -> np.ndarray:
        """
        Generate Pi-shaped membership function.
        
        Pi-shaped functions combine two sigmoidal functions to create
        a bell-like shape with more control over the shoulders.
        
        Args:
            x (np.ndarray): Universe of discourse
            params (Tuple[float, float, float, float]): (a, b, c, d) where:
                - a, b: parameters for left sigmoidal
                - c, d: parameters for right sigmoidal
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        a, b, c, d = params
        
        # Left half: increasing sigmoidal
        left_sigmoid = MembershipFunctions.sigmoidal_mf(x, (a, b))
        
        # Right half: decreasing sigmoidal  
        right_sigmoid = MembershipFunctions.sigmoidal_mf(x, (-c, d))
        
        # Combine using minimum operation
        mf = np.minimum(left_sigmoid, right_sigmoid)
        
        return mf
    
    @staticmethod
    def adaptive_triangular_mf(x: np.ndarray, base_params: Tuple[float, float, float], 
                             adaptation_factor: float = 0.0) -> np.ndarray:
        """
        Generate adaptive triangular membership function.
        
        This function can adjust its shape based on user behavior patterns,
        making the recommendation system more personalized over time.
        
        Args:
            x (np.ndarray): Universe of discourse
            base_params (Tuple[float, float, float]): Base triangular parameters
            adaptation_factor (float): Adaptation strength (-1.0 to 1.0)
                - Positive values make the function wider
                - Negative values make the function narrower
                
        Returns:
            np.ndarray: Membership degrees for each point in x
        """
        a, b, c = base_params
        
        # Clip adaptation factor to valid range
        adaptation_factor = np.clip(adaptation_factor, -0.9, 0.9)
        
        # Calculate adaptive parameters
        width_left = b - a
        width_right = c - b
        
        # Adjust widths based on adaptation factor
        new_a = a - (width_left * adaptation_factor * 0.5)
        new_c = c + (width_right * adaptation_factor * 0.5)
        
        # Ensure valid ordering
        new_a = min(new_a, b - 0.01)
        new_c = max(new_c, b + 0.01)
        
        return MembershipFunctions.triangular_mf(x, (new_a, b, new_c))
    
    @staticmethod
    def calculate_membership_degree(x_val: float, x_universe: np.ndarray, 
                                  mf_values: np.ndarray) -> float:
        """
        Calculate membership degree for a specific value using interpolation.
        
        Args:
            x_val (float): Input value to calculate membership for
            x_universe (np.ndarray): Universe of discourse
            mf_values (np.ndarray): Membership function values
            
        Returns:
            float: Membership degree (0.0 to 1.0)
        """
        # Handle edge cases
        if x_val <= x_universe[0]:
            return float(mf_values[0])
        if x_val >= x_universe[-1]:
            return float(mf_values[-1])
        
        # Linear interpolation
        membership = np.interp(x_val, x_universe, mf_values)
        
        return float(membership)
    
    @staticmethod
    def visualize_membership_functions(functions_dict: Dict[str, Dict], 
                                     title: str = "Membership Functions",
                                     save_path: str = None) -> None:
        """
        Visualize multiple membership functions on the same plot.
        
        Args:
            functions_dict (Dict[str, Dict]): Dictionary with function data
                Format: {
                    'function_name': {
                        'x': np.ndarray,
                        'y': np.ndarray,
                        'color': str (optional),
                        'style': str (optional)
                    }
                }
            title (str): Plot title
            save_path (str): Path to save the plot (optional)
        """
        plt.figure(figsize=(12, 8))
        
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']
        styles = ['-', '--', '-.', ':']
        
        for i, (name, data) in enumerate(functions_dict.items()):
            color = data.get('color', colors[i % len(colors)])
            style = data.get('style', styles[i % len(styles)])
            
            plt.plot(data['x'], data['y'], 
                    color=color, linestyle=style, linewidth=2.5, 
                    label=name, alpha=0.8)
        
        plt.xlabel('Universe of Discourse', fontweight='bold')
        plt.ylabel('Membership Degree', fontweight='bold')
        plt.title(title, fontweight='bold', fontsize=14)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.ylim(-0.05, 1.05)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.show()
    
    @staticmethod
    def analyze_membership_overlap(x: np.ndarray, mf1: np.ndarray, mf2: np.ndarray) -> Dict[str, float]:
        """
        Analyze overlap between two membership functions.
        
        Args:
            x (np.ndarray): Universe of discourse
            mf1 (np.ndarray): First membership function
            mf2 (np.ndarray): Second membership function
            
        Returns:
            Dict[str, float]: Analysis results including overlap area and maximum overlap
        """
        # Calculate overlap (minimum of both functions)
        overlap = np.minimum(mf1, mf2)
        
        # Calculate areas using trapezoidal integration
        dx = x[1] - x[0] if len(x) > 1 else 1.0
        
        overlap_area = np.trapz(overlap, dx=dx)
        mf1_area = np.trapz(mf1, dx=dx)
        mf2_area = np.trapz(mf2, dx=dx)
        
        # Calculate relative overlap
        total_area = mf1_area + mf2_area - overlap_area
        relative_overlap = overlap_area / total_area if total_area > 0 else 0.0
        
        # Find maximum overlap point
        max_overlap_idx = np.argmax(overlap)
        max_overlap_value = overlap[max_overlap_idx]
        max_overlap_x = x[max_overlap_idx]
        
        return {
            'overlap_area': overlap_area,
            'relative_overlap': relative_overlap,
            'max_overlap_value': max_overlap_value,
            'max_overlap_x': max_overlap_x,
            'mf1_area': mf1_area,
            'mf2_area': mf2_area
        }


class MovieRecommendationMF:
    """
    Specialized membership functions for movie recommendation domain.
    
    This class provides domain-specific membership functions that are
    optimized for movie recommendation scenarios.
    """
    
    @staticmethod
    def user_rating_mf(rating_history: List[float]) -> Dict[str, Tuple]:
        """
        Generate adaptive user rating membership function parameters based on user history.
        
        Args:
            rating_history (List[float]): User's historical ratings
            
        Returns:
            Dict[str, Tuple]: Membership function parameters for different rating levels
        """
        if not rating_history:
            # Default parameters if no history
            return {
                'low': (1, 1, 4),
                'medium': (2, 5.5, 8),
                'high': (6, 10, 10)
            }
        
        # Analyze user rating patterns
        ratings = np.array(rating_history)
        mean_rating = np.mean(ratings)
        std_rating = np.std(ratings)
        
        # Adaptive parameters based on user behavior
        if std_rating < 1.0:  # Conservative rater
            return {
                'low': (1, 1, mean_rating - 0.5),
                'medium': (mean_rating - 1, mean_rating, mean_rating + 1),
                'high': (mean_rating + 0.5, 10, 10)
            }
        else:  # Wide range rater
            return {
                'low': (1, 1, mean_rating - std_rating),
                'medium': (mean_rating - std_rating/2, mean_rating, mean_rating + std_rating/2),
                'high': (mean_rating + std_rating, 10, 10)
            }
    
    @staticmethod
    def genre_preference_mf(genre_scores: Dict[str, float]) -> Dict[str, Tuple]:
        """
        Generate genre preference membership function parameters.
        
        Args:
            genre_scores (Dict[str, float]): User's preference scores for different genres
            
        Returns:
            Dict[str, Tuple]: Membership function parameters for genre matching
        """
        if not genre_scores:
            # Default parameters
            return {
                'poor': (0, 0, 35),
                'moderate': (20, 50, 80),
                'excellent': (65, 100, 100)
            }
        
        scores = list(genre_scores.values())
        if not scores:
            return {
                'poor': (0, 0, 35),
                'moderate': (20, 50, 80),
                'excellent': (65, 100, 100)
            }
        
        # Adaptive thresholds based on user preferences
        min_score = min(scores)
        max_score = max(scores)
        mid_score = (min_score + max_score) / 2
        
        return {
            'poor': (0, min_score, mid_score),
            'moderate': (min_score, mid_score, max_score),
            'excellent': (mid_score, max_score, 100)
        }


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of membership function utilities.
    """
    
    print("Advanced Membership Functions for Movie Recommendation System")
    print("=" * 65)
    
    # Create test universe
    x = np.linspace(0, 10, 100)
    
    # Test different membership function types
    print("\n1. Testing Membership Function Types:")
    print("-" * 40)
    
    # Triangular
    tri_mf = MembershipFunctions.triangular_mf(x, (2, 5, 8))
    print(f"Triangular MF (2,5,8) at x=5: {MembershipFunctions.calculate_membership_degree(5.0, x, tri_mf):.3f}")
    
    # Trapezoidal
    trap_mf = MembershipFunctions.trapezoidal_mf(x, (1, 3, 7, 9))
    print(f"Trapezoidal MF (1,3,7,9) at x=5: {MembershipFunctions.calculate_membership_degree(5.0, x, trap_mf):.3f}")
    
    # Gaussian
    gauss_mf = MembershipFunctions.gaussian_mf(x, (5, 1.5))
    print(f"Gaussian MF (μ=5,σ=1.5) at x=5: {MembershipFunctions.calculate_membership_degree(5.0, x, gauss_mf):.3f}")
    
    # Test adaptive functions
    print("\n2. Testing Adaptive Functions:")
    print("-" * 40)
    
    # User rating adaptation
    rating_history = [7.5, 8.0, 7.0, 8.5, 7.5, 9.0]
    adaptive_params = MovieRecommendationMF.user_rating_mf(rating_history)
    print("Adaptive user rating parameters:")
    for level, params in adaptive_params.items():
        print(f"  {level}: {params}")
    
    # Membership function overlap analysis
    print("\n3. Membership Function Overlap Analysis:")
    print("-" * 40)
    
    overlap_analysis = MembershipFunctions.analyze_membership_overlap(x, tri_mf, gauss_mf)
    print(f"Overlap area: {overlap_analysis['overlap_area']:.3f}")
    print(f"Relative overlap: {overlap_analysis['relative_overlap']:.3f}")
    print(f"Max overlap at x={overlap_analysis['max_overlap_x']:.2f}: {overlap_analysis['max_overlap_value']:.3f}")
    
    # Visualization example (uncomment to show plots)
    # functions_dict = {
    #     'Triangular': {'x': x, 'y': tri_mf},
    #     'Trapezoidal': {'x': x, 'y': trap_mf},
    #     'Gaussian': {'x': x, 'y': gauss_mf}
    # }
    # MembershipFunctions.visualize_membership_functions(
    #     functions_dict, 
    #     "Comparison of Membership Function Types"
    # )
