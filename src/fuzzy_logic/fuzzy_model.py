"""
Fuzzy Logic Model Core for Movie Recommendation System

This module implements the complete fuzzy logic inference system, integrating:
- Fuzzy variables and membership functions
- Fuzzy rule evaluation and inference
- Defuzzification methods
- Complete Mamdani fuzzy inference system

The FuzzyMovieRecommender class serves as the main controller that orchestrates
the entire fuzzy logic process from fuzzification to defuzzification, providing
crisp recommendation scores for movies.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Any
import warnings
from dataclasses import dataclass
from enum import Enum

# Import our custom fuzzy logic components
try:
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl
    SKFUZZY_AVAILABLE = True
except ImportError:
    SKFUZZY_AVAILABLE = False
    print("Warning: scikit-fuzzy not available. Some features may be limited.")

from fuzzy_logic.variables import FuzzyVariables
from fuzzy_logic.membership_func import MembershipFunctions
from fuzzy_logic.rules import FuzzyRuleEngine, FuzzyCondition, RuleOperator

warnings.filterwarnings('ignore', category=RuntimeWarning)


class DefuzzificationMethod(Enum):
    """Enumeration of available defuzzification methods."""
    CENTROID = "centroid"
    BISECTOR = "bisector"
    MOM = "mean_of_maximum"  # Mean of Maximum
    SOM = "smallest_of_maximum"  # Smallest of Maximum
    LOM = "largest_of_maximum"  # Largest of Maximum


@dataclass
class RecommendationResult:
    """
    Data structure for recommendation results.
    
    Attributes:
        recommendation_score (float): Final crisp recommendation score (0-100)
        confidence_level (float): Confidence in the recommendation (0-1)
        activated_rules (Dict): Rules that contributed to the recommendation
        membership_degrees (Dict): Input membership degrees for all variables
        explanation (str): Human-readable explanation of the recommendation
        defuzzification_method (str): Method used for defuzzification
    """
    recommendation_score: float
    confidence_level: float
    activated_rules: Dict[str, List[Tuple[int, float]]]
    membership_degrees: Dict[str, Dict[str, float]]
    explanation: str
    defuzzification_method: str


class FuzzyMovieRecommender:
    """
    Complete fuzzy logic movie recommendation system.
    
    This class implements a full Mamdani fuzzy inference system that:
    1. Takes crisp inputs (user rating, actor popularity, genre match)
    2. Fuzzifies inputs using membership functions
    3. Evaluates fuzzy rules to determine rule activations
    4. Aggregates rule consequents
    5. Defuzzifies to produce crisp recommendation scores
    
    The system is designed to be interpretable, allowing users to understand
    why specific recommendations were made.
    """
    
    def __init__(self, defuzzification_method: DefuzzificationMethod = DefuzzificationMethod.CENTROID):
        """
        Initialize the fuzzy movie recommender system.
        
        Args:
            defuzzification_method (DefuzzificationMethod): Method for defuzzification
        """
        self.defuzzification_method = defuzzification_method
        
        # Initialize fuzzy logic components
        self.fuzzy_variables = FuzzyVariables()
        self.membership_functions = MembershipFunctions()
        self.rule_engine = FuzzyRuleEngine()
        
        # Create the rule base
        self.rule_engine.create_movie_recommendation_rules()
        
        # Get variables for internal use
        self.variables = self.fuzzy_variables.get_variables()
        
        # Initialize system state
        self.last_recommendation = None
        self.recommendation_history = []
        
        print(f"Fuzzy Movie Recommender initialized with {len(self.rule_engine.rules)} rules")
        print(f"Defuzzification method: {defuzzification_method.value}")
    
    def fuzzify_inputs(self, user_rating: float, actor_popularity: float, 
                      genre_match: float) -> Dict[str, Dict[str, float]]:
        """
        Convert crisp inputs to fuzzy membership degrees.
        
        This is the fuzzification step where crisp input values are converted
        to membership degrees across all linguistic terms for each variable.
        
        Args:
            user_rating (float): User's historical rating pattern (1-10)
            actor_popularity (float): Actor popularity score (0-100)
            genre_match (float): Genre matching score (0-100)
        
        Returns:
            Dict[str, Dict[str, float]]: Membership degrees for all variables and terms
        """
        
        # Validate inputs
        self._validate_inputs(user_rating, actor_popularity, genre_match)
        
        membership_degrees = {}
        
        # Fuzzify user rating (1-10 scale)
        membership_degrees['user_rating'] = {}
        for term in self.variables['user_rating'].terms:
            membership = self._calculate_membership(
                user_rating,
                self.variables['user_rating'].universe,
                self.variables['user_rating'][term].mf
            )
            membership_degrees['user_rating'][term] = membership
        
        # Fuzzify actor popularity (0-100 scale)
        membership_degrees['actor_popularity'] = {}
        for term in self.variables['actor_popularity'].terms:
            membership = self._calculate_membership(
                actor_popularity,
                self.variables['actor_popularity'].universe,
                self.variables['actor_popularity'][term].mf
            )
            membership_degrees['actor_popularity'][term] = membership
        
        # Fuzzify genre match (0-100 scale)
        membership_degrees['genre_match'] = {}
        for term in self.variables['genre_match'].terms:
            membership = self._calculate_membership(
                genre_match,
                self.variables['genre_match'].universe,
                self.variables['genre_match'][term].mf
            )
            membership_degrees['genre_match'][term] = membership
        
        return membership_degrees
    
    def recommend_movie(self, user_rating: float, actor_popularity: float, 
                       genre_match: float, include_explanation: bool = True) -> RecommendationResult:
        """
        Generate a movie recommendation using fuzzy logic inference.
        
        This is the main method that performs the complete fuzzy inference process:
        1. Fuzzification of inputs
        2. Rule evaluation and aggregation
        3. Defuzzification to crisp output
        4. Confidence calculation
        5. Explanation generation
        
        Args:
            user_rating (float): User's historical rating pattern (1-10)
            actor_popularity (float): Actor popularity score (0-100)
            genre_match (float): Genre matching score (0-100)
            include_explanation (bool): Whether to generate detailed explanations
        
        Returns:
            RecommendationResult: Complete recommendation with explanation
        """
        
        # Step 1: Fuzzification
        membership_degrees = self.fuzzify_inputs(user_rating, actor_popularity, genre_match)
        
        # Step 2: Rule Evaluation
        activated_rules = self.rule_engine.evaluate_all_rules(membership_degrees)
        
        # Step 3: Aggregation and Defuzzification
        recommendation_score = self._defuzzify_output(activated_rules)
        
        # Step 4: Calculate Confidence
        confidence_level = self._calculate_confidence(activated_rules, membership_degrees)
        
        # Step 5: Generate Explanation
        explanation = ""
        if include_explanation:
            explanation = self._generate_explanation(
                activated_rules, membership_degrees, 
                user_rating, actor_popularity, genre_match
            )
        
        # Create result object
        result = RecommendationResult(
            recommendation_score=recommendation_score,
            confidence_level=confidence_level,
            activated_rules=activated_rules,
            membership_degrees=membership_degrees,
            explanation=explanation,
            defuzzification_method=self.defuzzification_method.value
        )
        
        # Store for history and analysis
        self.last_recommendation = result
        self.recommendation_history.append(result)
        
        return result
    
    def batch_recommend(self, input_data: List[Tuple[float, float, float]]) -> List[RecommendationResult]:
        """
        Generate recommendations for multiple movies in batch.
        
        Args:
            input_data (List[Tuple[float, float, float]]): List of (user_rating, actor_popularity, genre_match)
        
        Returns:
            List[RecommendationResult]: List of recommendation results
        """
        results = []
        
        for user_rating, actor_popularity, genre_match in input_data:
            try:
                result = self.recommend_movie(
                    user_rating, actor_popularity, genre_match, 
                    include_explanation=False  # Skip explanations for batch processing
                )
                results.append(result)
            except Exception as e:
                print(f"Error processing input ({user_rating}, {actor_popularity}, {genre_match}): {e}")
                # Create a default "not recommended" result
                results.append(RecommendationResult(
                    recommendation_score=0.0,
                    confidence_level=0.0,
                    activated_rules={},
                    membership_degrees={},
                    explanation=f"Error in processing: {e}",
                    defuzzification_method=self.defuzzification_method.value
                ))
        
        return results
    
    def _validate_inputs(self, user_rating: float, actor_popularity: float, genre_match: float) -> None:
        """Validate input parameters."""
        if not (1.0 <= user_rating <= 10.0):
            raise ValueError(f"User rating must be between 1.0 and 10.0, got: {user_rating}")
        
        if not (0.0 <= actor_popularity <= 100.0):
            raise ValueError(f"Actor popularity must be between 0.0 and 100.0, got: {actor_popularity}")
        
        if not (0.0 <= genre_match <= 100.0):
            raise ValueError(f"Genre match must be between 0.0 and 100.0, got: {genre_match}")
    
    def _calculate_membership(self, value: float, universe: np.ndarray, mf: np.ndarray) -> float:
        """Calculate membership degree for a specific value."""
        return float(self.membership_functions.calculate_membership_degree(value, universe, mf))
    
    def _defuzzify_output(self, activated_rules: Dict[str, List[Tuple[int, float]]]) -> float:
        """
        Defuzzify the aggregated fuzzy output to a crisp recommendation score.
        
        This method implements various defuzzification strategies to convert
        the fuzzy recommendation into a crisp numerical score.
        
        Args:
            activated_rules (Dict[str, List[Tuple[int, float]]]): Activated rules by consequent
        
        Returns:
            float: Crisp recommendation score (0-100)
        """
        
        if not activated_rules:
            return 0.0  # No rules activated
        
        # Get the recommendation variable universe and membership functions
        rec_var = self.variables['recommendation']
        universe = rec_var.universe
        
        # Initialize aggregated membership function (using maximum aggregation)
        aggregated_mf = np.zeros_like(universe, dtype=float)
        
        # Aggregate all activated consequents
        for consequent_term, rule_activations in activated_rules.items():
            if consequent_term in rec_var.terms:
                # Get the membership function for this consequent
                consequent_mf = rec_var[consequent_term].mf
                
                # Find the maximum activation strength for this consequent
                max_activation = max(activation for _, activation in rule_activations)
                
                # Clip the membership function at the activation level (Mamdani implication)
                clipped_mf = np.minimum(consequent_mf, max_activation)
                
                # Aggregate using maximum operator
                aggregated_mf = np.maximum(aggregated_mf, clipped_mf)
        
        # Apply defuzzification method
        if self.defuzzification_method == DefuzzificationMethod.CENTROID:
            return self._centroid_defuzzification(universe, aggregated_mf)
        elif self.defuzzification_method == DefuzzificationMethod.BISECTOR:
            return self._bisector_defuzzification(universe, aggregated_mf)
        elif self.defuzzification_method == DefuzzificationMethod.MOM:
            return self._mom_defuzzification(universe, aggregated_mf)
        elif self.defuzzification_method == DefuzzificationMethod.SOM:
            return self._som_defuzzification(universe, aggregated_mf)
        elif self.defuzzification_method == DefuzzificationMethod.LOM:
            return self._lom_defuzzification(universe, aggregated_mf)
        else:
            # Default to centroid
            return self._centroid_defuzzification(universe, aggregated_mf)
    
    def _centroid_defuzzification(self, universe: np.ndarray, mf: np.ndarray) -> float:
        """Centroid defuzzification method."""
        if np.sum(mf) == 0:
            return 0.0
        
        numerator = np.sum(universe * mf)
        denominator = np.sum(mf)
        
        return float(numerator / denominator)
    
    def _bisector_defuzzification(self, universe: np.ndarray, mf: np.ndarray) -> float:
        """Bisector defuzzification method."""
        total_area = np.trapz(mf, universe)
        if total_area == 0:
            return 0.0
        
        half_area = total_area / 2
        cumulative_area = 0
        
        for i in range(len(universe) - 1):
            segment_area = (mf[i] + mf[i + 1]) * (universe[i + 1] - universe[i]) / 2
            cumulative_area += segment_area
            
            if cumulative_area >= half_area:
                return float(universe[i])
        
        return float(universe[-1])
    
    def _mom_defuzzification(self, universe: np.ndarray, mf: np.ndarray) -> float:
        """Mean of Maximum defuzzification method."""
        max_val = np.max(mf)
        if max_val == 0:
            return 0.0
        
        max_indices = np.where(mf == max_val)[0]
        return float(np.mean(universe[max_indices]))
    
    def _som_defuzzification(self, universe: np.ndarray, mf: np.ndarray) -> float:
        """Smallest of Maximum defuzzification method."""
        max_val = np.max(mf)
        if max_val == 0:
            return 0.0
        
        max_indices = np.where(mf == max_val)[0]
        return float(universe[max_indices[0]])
    
    def _lom_defuzzification(self, universe: np.ndarray, mf: np.ndarray) -> float:
        """Largest of Maximum defuzzification method."""
        max_val = np.max(mf)
        if max_val == 0:
            return 0.0
        
        max_indices = np.where(mf == max_val)[0]
        return float(universe[max_indices[-1]])
    
    def _calculate_confidence(self, activated_rules: Dict[str, List[Tuple[int, float]]], 
                            membership_degrees: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate confidence in the recommendation based on rule activations and input certainty.
        
        Args:
            activated_rules (Dict): Activated rules
            membership_degrees (Dict): Input membership degrees
        
        Returns:
            float: Confidence level (0.0 to 1.0)
        """
        
        if not activated_rules:
            return 0.0
        
        # Factor 1: Maximum rule activation strength
        max_activation = 0.0
        for rule_list in activated_rules.values():
            for _, strength in rule_list:
                max_activation = max(max_activation, strength)
        
        # Factor 2: Input certainty (how clearly defined the inputs are)
        input_certainty = 0.0
        total_vars = 0
        
        for var_name, terms in membership_degrees.items():
            max_membership = max(terms.values())
            input_certainty += max_membership
            total_vars += 1
        
        if total_vars > 0:
            input_certainty /= total_vars
        
        # Factor 3: Number of activated rules (more rules = higher confidence)
        total_activated = sum(len(rules) for rules in activated_rules.values())
        rule_diversity = min(1.0, total_activated / 5.0)  # Normalize to max of 5 rules
        
        # Combine factors with weights
        confidence = (
            0.5 * max_activation +
            0.3 * input_certainty +
            0.2 * rule_diversity
        )
        
        return min(1.0, confidence)
    
    def _generate_explanation(self, activated_rules: Dict[str, List[Tuple[int, float]]], 
                            membership_degrees: Dict[str, Dict[str, float]],
                            user_rating: float, actor_popularity: float, 
                            genre_match: float) -> str:
        """Generate human-readable explanation for the recommendation."""
        
        explanation_parts = []
        
        # Input analysis
        explanation_parts.append("INPUT ANALYSIS:")
        explanation_parts.append(f"• User Rating: {user_rating:.1f}/10")
        explanation_parts.append(f"• Actor Popularity: {actor_popularity:.1f}/100")
        explanation_parts.append(f"• Genre Match: {genre_match:.1f}/100")
        explanation_parts.append("")
        
        # Fuzzification results
        explanation_parts.append("FUZZIFICATION RESULTS:")
        for var_name, terms in membership_degrees.items():
            var_display = var_name.replace('_', ' ').title()
            explanation_parts.append(f"• {var_display}:")
            
            # Sort terms by membership degree
            sorted_terms = sorted(terms.items(), key=lambda x: x[1], reverse=True)
            for term, membership in sorted_terms[:2]:  # Show top 2 terms
                if membership > 0.1:  # Only show significant memberships
                    explanation_parts.append(f"  - {term}: {membership:.2f}")
        
        explanation_parts.append("")
        
        # Rule activations
        if activated_rules:
            explanation_parts.append("ACTIVATED RULES:")
            
            # Get rule explanations
            rule_explanations = self.rule_engine.get_rule_explanations(activated_rules, top_n=3)
            
            for consequent, explanations in rule_explanations.items():
                consequent_display = consequent.replace('_', ' ').title()
                explanation_parts.append(f"• {consequent_display}:")
                
                for exp in explanations:
                    strength_pct = exp['strength'] * 100
                    explanation_parts.append(f"  - {exp['description']} (Strength: {strength_pct:.1f}%)")
        else:
            explanation_parts.append("No rules were activated with the given inputs.")
        
        return "\n".join(explanation_parts)
    
    def visualize_recommendation(self, result: RecommendationResult, save_path: str = None) -> None:
        """
        Create visualization of the recommendation process.
        
        Args:
            result (RecommendationResult): Recommendation result to visualize
            save_path (str): Path to save the visualization (optional)
        """
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Fuzzy Logic Movie Recommendation Analysis\nScore: {result.recommendation_score:.1f}/100', 
                    fontsize=16, fontweight='bold')
        
        # Plot 1: Input Membership Degrees
        ax1 = axes[0, 0]
        variables = list(result.membership_degrees.keys())
        
        for i, (var_name, terms) in enumerate(result.membership_degrees.items()):
            terms_list = list(terms.keys())
            values = list(terms.values())
            
            x_pos = np.arange(len(terms_list)) + i * 0.25
            ax1.bar(x_pos, values, width=0.2, label=var_name.replace('_', ' ').title(), alpha=0.7)
        
        ax1.set_title('Input Membership Degrees', fontweight='bold')
        ax1.set_ylabel('Membership Degree')
        ax1.set_xlabel('Linguistic Terms')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Rule Activations
        ax2 = axes[0, 1]
        if result.activated_rules:
            consequents = list(result.activated_rules.keys())
            max_strengths = [max(strength for _, strength in rules) 
                           for rules in result.activated_rules.values()]
            
            bars = ax2.bar(consequents, max_strengths, alpha=0.7, color=['red', 'orange', 'lightgreen', 'green'])
            ax2.set_title('Maximum Rule Activation Strengths', fontweight='bold')
            ax2.set_ylabel('Activation Strength')
            ax2.set_xlabel('Recommendation Level')
            
            # Rotate x-axis labels for better readability
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        else:
            ax2.text(0.5, 0.5, 'No Rules Activated', ha='center', va='center', 
                    transform=ax2.transAxes, fontsize=14)
            ax2.set_title('Rule Activations', fontweight='bold')
        
        # Plot 3: Confidence Breakdown
        ax3 = axes[1, 0]
        confidence_factors = ['Overall Confidence', 'Input Certainty', 'Rule Strength']
        confidence_values = [result.confidence_level, 0.8, 0.7]  # Placeholder values
        
        ax3.bar(confidence_factors, confidence_values, alpha=0.7, color=['blue', 'cyan', 'lightblue'])
        ax3.set_title('Confidence Analysis', fontweight='bold')
        ax3.set_ylabel('Confidence Level')
        ax3.set_ylim(0, 1)
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        # Plot 4: Recommendation Score Gauge
        ax4 = axes[1, 1]
        
        # Create a simple gauge-like visualization
        score = result.recommendation_score
        colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
        ranges = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100)]
        
        for i, (start, end) in enumerate(ranges):
            if start <= score <= end:
                color = colors[i]
                break
        else:
            color = 'gray'
        
        # Draw gauge
        theta = np.linspace(0, np.pi, 100)
        r = 1
        ax4.plot(r * np.cos(theta), r * np.sin(theta), 'k-', linewidth=2)
        
        # Score indicator
        score_angle = np.pi * (1 - score / 100)
        ax4.arrow(0, 0, 0.8 * np.cos(score_angle), 0.8 * np.sin(score_angle), 
                 head_width=0.1, head_length=0.1, fc=color, ec=color, linewidth=3)
        
        ax4.text(0, -0.3, f'{score:.1f}/100', ha='center', va='center', 
                fontsize=16, fontweight='bold')
        ax4.set_xlim(-1.2, 1.2)
        ax4.set_ylim(-0.5, 1.2)
        ax4.set_aspect('equal')
        ax4.axis('off')
        ax4.set_title('Recommendation Score', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")
        
        plt.show()
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive information about the fuzzy system."""
        
        return {
            'total_rules': len(self.rule_engine.rules),
            'variables': list(self.variables.keys()),
            'defuzzification_method': self.defuzzification_method.value,
            'recommendation_history_count': len(self.recommendation_history),
            'rule_statistics': self.rule_engine.get_rule_statistics(),
            'variable_universes': {
                name: {'min': float(var.universe.min()), 'max': float(var.universe.max())}
                for name, var in self.variables.items()
            }
        }
    
    def print_system_summary(self) -> None:
        """Print a comprehensive summary of the fuzzy system."""
        
        info = self.get_system_info()
        
        print("="*80)
        print("FUZZY MOVIE RECOMMENDATION SYSTEM SUMMARY")
        print("="*80)
        
        print(f"\nSystem Configuration:")
        print(f"  • Total Fuzzy Rules: {info['total_rules']}")
        print(f"  • Fuzzy Variables: {', '.join(info['variables'])}")
        print(f"  • Defuzzification Method: {info['defuzzification_method']}")
        print(f"  • Recommendations Generated: {info['recommendation_history_count']}")
        
        print(f"\nVariable Universes:")
        for var_name, universe in info['variable_universes'].items():
            print(f"  • {var_name.replace('_', ' ').title()}: [{universe['min']:.1f}, {universe['max']:.1f}]")
        
        if info['recommendation_history_count'] > 0:
            avg_score = np.mean([r.recommendation_score for r in self.recommendation_history])
            avg_confidence = np.mean([r.confidence_level for r in self.recommendation_history])
            
            print(f"\nPerformance Statistics:")
            print(f"  • Average Recommendation Score: {avg_score:.2f}")
            print(f"  • Average Confidence Level: {avg_confidence:.2f}")
        
        print("="*80)


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the complete fuzzy movie recommendation system.
    """
    
    print("Complete Fuzzy Logic Movie Recommendation System")
    print("=" * 50)
    
    # Initialize the recommender
    recommender = FuzzyMovieRecommender(DefuzzificationMethod.CENTROID)
    
    # Print system summary
    recommender.print_system_summary()
    
    # Test single recommendation
    print("\n" + "="*60)
    print("SINGLE MOVIE RECOMMENDATION TEST")
    print("="*60)
    
    # Test case: High-quality movie with famous actors in preferred genre
    result = recommender.recommend_movie(
        user_rating=8.5,
        actor_popularity=85.0,
        genre_match=90.0
    )
    
    print(f"Recommendation Score: {result.recommendation_score:.2f}/100")
    print(f"Confidence Level: {result.confidence_level:.2f}")
    print(f"Defuzzification Method: {result.defuzzification_method}")
    
    print("\nExplanation:")
    print(result.explanation)
    
    # Test batch recommendations
    print("\n" + "="*60)
    print("BATCH RECOMMENDATION TEST")
    print("="*60)
    
    test_cases = [
        (9.0, 95.0, 95.0),  # Perfect movie
        (3.0, 10.0, 20.0),  # Poor movie
        (7.0, 60.0, 70.0),  # Good movie
        (5.0, 85.0, 30.0),  # Famous actors, poor genre match
        (8.0, 20.0, 95.0),  # Great content, unknown actors
    ]
    
    batch_results = recommender.batch_recommend(test_cases)
    
    print("Batch Results:")
    print("-" * 40)
    for i, (inputs, result) in enumerate(zip(test_cases, batch_results)):
        print(f"Movie {i+1}: Inputs{inputs} → Score: {result.recommendation_score:.1f}, "
              f"Confidence: {result.confidence_level:.2f}")
    
    # System performance summary
    print("\n" + "="*60)
    print("FINAL SYSTEM SUMMARY")
    print("="*60)
    
    recommender.print_system_summary()
    
    # Visualization example (uncomment to show plots)
    # recommender.visualize_recommendation(result, save_path="recommendation_analysis.png")
