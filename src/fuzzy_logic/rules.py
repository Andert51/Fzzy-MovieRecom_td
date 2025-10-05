"""
Fuzzy Rules Module for Movie Recommendation System

This module implements the fuzzy inference rules that form the core decision-making
logic of the movie recommendation system. The rules capture expert knowledge about
how different factors (user ratings, actor popularity, genre matching) combine
to generate movie recommendations.

The rules are implemented using Mamdani fuzzy inference, providing interpretable
and adjustable recommendation logic that can be easily modified or extended.

Rule Structure:
IF (user_rating is X) AND/OR (actor_popularity is Y) AND/OR (genre_match is Z)
THEN (recommendation is W)
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import itertools
from dataclasses import dataclass
from enum import Enum


class RuleOperator(Enum):
    """Enumeration of fuzzy rule operators."""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class RuleConfidence(Enum):
    """Enumeration of rule confidence levels."""
    HIGH = 1.0
    MEDIUM = 0.8
    LOW = 0.6


@dataclass
class FuzzyCondition:
    """
    Represents a single fuzzy condition in a rule.
    
    Attributes:
        variable_name (str): Name of the fuzzy variable (e.g., 'user_rating')
        linguistic_term (str): Linguistic term (e.g., 'high', 'low')
        negated (bool): Whether the condition is negated (NOT)
    """
    variable_name: str
    linguistic_term: str
    negated: bool = False
    
    def __str__(self) -> str:
        negation = "NOT " if self.negated else ""
        return f"{negation}{self.variable_name} is {self.linguistic_term}"


@dataclass
class FuzzyRule:
    """
    Represents a complete fuzzy rule with antecedents and consequent.
    
    Attributes:
        rule_id (int): Unique identifier for the rule
        antecedents (List[FuzzyCondition]): List of antecedent conditions
        consequent (FuzzyCondition): Consequent condition
        operator (RuleOperator): Operator connecting antecedents (AND/OR)
        confidence (float): Confidence level of the rule (0.0 to 1.0)
        description (str): Human-readable description of the rule
    """
    rule_id: int
    antecedents: List[FuzzyCondition]
    consequent: FuzzyCondition
    operator: RuleOperator = RuleOperator.AND
    confidence: float = 1.0
    description: str = ""
    
    def __str__(self) -> str:
        antecedent_str = f" {self.operator.value} ".join(str(ant) for ant in self.antecedents)
        return f"Rule {self.rule_id}: IF {antecedent_str} THEN {self.consequent}"


class FuzzyRuleEngine:
    """
    Advanced fuzzy rule engine for movie recommendations.
    
    This class manages the creation, evaluation, and execution of fuzzy rules.
    It implements Mamdani fuzzy inference with support for multiple operators
    and confidence-weighted rule evaluation.
    """
    
    def __init__(self):
        """Initialize the fuzzy rule engine."""
        self.rules: List[FuzzyRule] = []
        self.rule_statistics: Dict[int, Dict] = {}
        
    def create_movie_recommendation_rules(self) -> None:
        """
        Create comprehensive fuzzy rules for movie recommendation.
        
        This method defines the complete rule base that captures expert knowledge
        about movie preferences. The rules cover various scenarios from highly
        recommended to not recommended movies.
        
        Rule Categories:
        1. Highly Recommended Rules (Score: 80-100)
        2. Recommended Rules (Score: 50-75)  
        3. Possibly Recommended Rules (Score: 15-40)
        4. Not Recommended Rules (Score: 0-25)
        """
        
        # Clear existing rules
        self.rules.clear()
        
        # Category 1: HIGHLY RECOMMENDED RULES
        # These rules identify movies with the highest recommendation potential
        
        # Rule 1: Perfect combination - high rating, famous actors, excellent genre match
        self.add_rule(
            rule_id=1,
            antecedents=[
                FuzzyCondition("user_rating", "high"),
                FuzzyCondition("actor_popularity", "famous"),
                FuzzyCondition("genre_match", "excellent")
            ],
            consequent=FuzzyCondition("recommendation", "highly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.HIGH.value,
            description="Perfect match: High user ratings, famous actors, and excellent genre alignment"
        )
        
        # Rule 2: High ratings with excellent genre match (even with unknown actors)
        self.add_rule(
            rule_id=2,
            antecedents=[
                FuzzyCondition("user_rating", "high"),
                FuzzyCondition("genre_match", "excellent")
            ],
            consequent=FuzzyCondition("recommendation", "highly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.HIGH.value,
            description="Content-driven recommendation: High ratings with perfect genre match"
        )
        
        # Rule 3: Famous actors with excellent genre match
        self.add_rule(
            rule_id=3,
            antecedents=[
                FuzzyCondition("actor_popularity", "famous"),
                FuzzyCondition("genre_match", "excellent")
            ],
            consequent=FuzzyCondition("recommendation", "highly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Star power with genre alignment: Famous actors in preferred genres"
        )
        
        # Category 2: RECOMMENDED RULES
        # These rules identify movies with good recommendation potential
        
        # Rule 4: High ratings with known actors
        self.add_rule(
            rule_id=4,
            antecedents=[
                FuzzyCondition("user_rating", "high"),
                FuzzyCondition("actor_popularity", "known")
            ],
            consequent=FuzzyCondition("recommendation", "recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.HIGH.value,
            description="Quality with recognition: High ratings and established actors"
        )
        
        # Rule 5: Medium ratings with famous actors and excellent genre match
        self.add_rule(
            rule_id=5,
            antecedents=[
                FuzzyCondition("user_rating", "medium"),
                FuzzyCondition("actor_popularity", "famous"),
                FuzzyCondition("genre_match", "excellent")
            ],
            consequent=FuzzyCondition("recommendation", "recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Balanced recommendation: Decent ratings, star power, and genre match"
        )
        
        # Rule 6: Medium ratings with excellent genre match
        self.add_rule(
            rule_id=6,
            antecedents=[
                FuzzyCondition("user_rating", "medium"),
                FuzzyCondition("genre_match", "excellent")
            ],
            consequent=FuzzyCondition("recommendation", "recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Genre-focused recommendation: Decent ratings with perfect genre alignment"
        )
        
        # Rule 7: High ratings with moderate genre match
        self.add_rule(
            rule_id=7,
            antecedents=[
                FuzzyCondition("user_rating", "high"),
                FuzzyCondition("genre_match", "moderate")
            ],
            consequent=FuzzyCondition("recommendation", "recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Quality-driven recommendation: High ratings compensate for moderate genre match"
        )
        
        # Category 3: POSSIBLY RECOMMENDED RULES
        # These rules identify movies with moderate recommendation potential
        
        # Rule 8: Medium ratings with known actors and moderate genre match
        self.add_rule(
            rule_id=8,
            antecedents=[
                FuzzyCondition("user_rating", "medium"),
                FuzzyCondition("actor_popularity", "known"),
                FuzzyCondition("genre_match", "moderate")
            ],
            consequent=FuzzyCondition("recommendation", "possibly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Moderate appeal: Average ratings with known actors and genre alignment"
        )
        
        # Rule 9: Famous actors with moderate genre match (regardless of ratings)
        self.add_rule(
            rule_id=9,
            antecedents=[
                FuzzyCondition("actor_popularity", "famous"),
                FuzzyCondition("genre_match", "moderate")
            ],
            consequent=FuzzyCondition("recommendation", "possibly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.LOW.value,
            description="Star-driven possibility: Famous actors might overcome genre mismatch"
        )
        
        # Rule 10: High ratings with poor genre match
        self.add_rule(
            rule_id=10,
            antecedents=[
                FuzzyCondition("user_rating", "high"),
                FuzzyCondition("genre_match", "poor")
            ],
            consequent=FuzzyCondition("recommendation", "possibly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.LOW.value,
            description="Quality exploration: High ratings might indicate worth despite genre mismatch"
        )
        
        # Rule 11: Medium ratings with famous actors (poor genre match)
        self.add_rule(
            rule_id=11,
            antecedents=[
                FuzzyCondition("user_rating", "medium"),
                FuzzyCondition("actor_popularity", "famous")
            ],
            consequent=FuzzyCondition("recommendation", "possibly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.LOW.value,
            description="Celebrity factor: Famous actors with decent ratings"
        )
        
        # Category 4: NOT RECOMMENDED RULES
        # These rules identify movies with low recommendation potential
        
        # Rule 12: Low ratings with poor genre match
        self.add_rule(
            rule_id=12,
            antecedents=[
                FuzzyCondition("user_rating", "low"),
                FuzzyCondition("genre_match", "poor")
            ],
            consequent=FuzzyCondition("recommendation", "not_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.HIGH.value,
            description="Clear rejection: Low ratings and poor genre alignment"
        )
        
        # Rule 13: Low ratings with unknown actors
        self.add_rule(
            rule_id=13,
            antecedents=[
                FuzzyCondition("user_rating", "low"),
                FuzzyCondition("actor_popularity", "unknown")
            ],
            consequent=FuzzyCondition("recommendation", "not_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.HIGH.value,
            description="Risk avoidance: Low ratings with unknown actors"
        )
        
        # Rule 14: Low ratings with known actors and poor genre match
        self.add_rule(
            rule_id=14,
            antecedents=[
                FuzzyCondition("user_rating", "low"),
                FuzzyCondition("actor_popularity", "known"),
                FuzzyCondition("genre_match", "poor")
            ],
            consequent=FuzzyCondition("recommendation", "not_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.MEDIUM.value,
            description="Multiple negatives: Low ratings and poor genre match despite known actors"
        )
        
        # Special Rules for Edge Cases
        
        # Rule 15: Exploration rule - unknown actors with excellent genre match and medium+ ratings
        self.add_rule(
            rule_id=15,
            antecedents=[
                FuzzyCondition("actor_popularity", "unknown"),
                FuzzyCondition("genre_match", "excellent"),
                FuzzyCondition("user_rating", "medium")
            ],
            consequent=FuzzyCondition("recommendation", "possibly_recommended"),
            operator=RuleOperator.AND,
            confidence=RuleConfidence.LOW.value,
            description="Discovery opportunity: Unknown actors with perfect genre match and decent ratings"
        )
        
        print(f"Created {len(self.rules)} fuzzy rules for movie recommendation")
        self._validate_rules()
    
    def add_rule(self, rule_id: int, antecedents: List[FuzzyCondition], 
                 consequent: FuzzyCondition, operator: RuleOperator = RuleOperator.AND,
                 confidence: float = 1.0, description: str = "") -> None:
        """
        Add a new fuzzy rule to the rule base.
        
        Args:
            rule_id (int): Unique identifier for the rule
            antecedents (List[FuzzyCondition]): List of antecedent conditions
            consequent (FuzzyCondition): Consequent condition
            operator (RuleOperator): Operator connecting antecedents
            confidence (float): Confidence level (0.0 to 1.0)
            description (str): Human-readable description
        """
        
        # Validate rule components
        if not antecedents:
            raise ValueError(f"Rule {rule_id}: At least one antecedent is required")
        
        if not (0.0 <= confidence <= 1.0):
            raise ValueError(f"Rule {rule_id}: Confidence must be between 0.0 and 1.0")
        
        # Check for duplicate rule IDs
        if any(rule.rule_id == rule_id for rule in self.rules):
            raise ValueError(f"Rule ID {rule_id} already exists")
        
        # Create and add the rule
        rule = FuzzyRule(
            rule_id=rule_id,
            antecedents=antecedents,
            consequent=consequent,
            operator=operator,
            confidence=confidence,
            description=description
        )
        
        self.rules.append(rule)
        
        # Initialize statistics tracking
        self.rule_statistics[rule_id] = {
            'activation_count': 0,
            'average_activation_strength': 0.0,
            'total_activation_strength': 0.0
        }
    
    def evaluate_rule(self, rule: FuzzyRule, input_memberships: Dict[str, Dict[str, float]]) -> float:
        """
        Evaluate a single fuzzy rule given input membership degrees.
        
        Args:
            rule (FuzzyRule): The rule to evaluate
            input_memberships (Dict[str, Dict[str, float]]): Input membership degrees
                Format: {variable_name: {linguistic_term: membership_degree}}
        
        Returns:
            float: Rule activation strength (0.0 to 1.0)
        """
        
        # Calculate membership degrees for all antecedents
        antecedent_memberships = []
        
        for condition in rule.antecedents:
            var_name = condition.variable_name
            term = condition.linguistic_term
            
            # Get membership degree
            if var_name in input_memberships and term in input_memberships[var_name]:
                membership = input_memberships[var_name][term]
                
                # Apply negation if needed
                if condition.negated:
                    membership = 1.0 - membership
                    
                antecedent_memberships.append(membership)
            else:
                # Missing membership - rule cannot fire
                return 0.0
        
        # Combine antecedents using the specified operator
        if rule.operator == RuleOperator.AND:
            # AND operation: minimum of all memberships
            rule_strength = min(antecedent_memberships)
        elif rule.operator == RuleOperator.OR:
            # OR operation: maximum of all memberships
            rule_strength = max(antecedent_memberships)
        else:
            raise ValueError(f"Unsupported operator: {rule.operator}")
        
        # Apply rule confidence
        final_strength = rule_strength * rule.confidence
        
        # Update statistics
        self._update_rule_statistics(rule.rule_id, final_strength)
        
        return final_strength
    
    def evaluate_all_rules(self, input_memberships: Dict[str, Dict[str, float]]) -> Dict[str, List[Tuple[int, float]]]:
        """
        Evaluate all rules and return activation strengths grouped by consequent.
        
        Args:
            input_memberships (Dict[str, Dict[str, float]]): Input membership degrees
        
        Returns:
            Dict[str, List[Tuple[int, float]]]: Activated rules grouped by consequent
                Format: {consequent_term: [(rule_id, activation_strength), ...]}
        """
        
        consequent_activations = {}
        
        for rule in self.rules:
            activation_strength = self.evaluate_rule(rule, input_memberships)
            
            if activation_strength > 0.0:  # Only include activated rules
                consequent_term = rule.consequent.linguistic_term
                
                if consequent_term not in consequent_activations:
                    consequent_activations[consequent_term] = []
                
                consequent_activations[consequent_term].append((rule.rule_id, activation_strength))
        
        # Sort by activation strength (descending)
        for term in consequent_activations:
            consequent_activations[term].sort(key=lambda x: x[1], reverse=True)
        
        return consequent_activations
    
    def get_rule_explanations(self, activated_rules: Dict[str, List[Tuple[int, float]]], 
                            top_n: int = 3) -> Dict[str, List[Dict]]:
        """
        Get human-readable explanations for activated rules.
        
        Args:
            activated_rules (Dict[str, List[Tuple[int, float]]]): Activated rules by consequent
            top_n (int): Number of top rules to explain per consequent
        
        Returns:
            Dict[str, List[Dict]]: Explanations grouped by consequent
        """
        
        explanations = {}
        
        for consequent_term, rule_activations in activated_rules.items():
            explanations[consequent_term] = []
            
            # Get top N rules for this consequent
            top_rules = rule_activations[:top_n]
            
            for rule_id, strength in top_rules:
                # Find the rule
                rule = next((r for r in self.rules if r.rule_id == rule_id), None)
                if rule:
                    explanations[consequent_term].append({
                        'rule_id': rule_id,
                        'strength': strength,
                        'description': rule.description,
                        'rule_text': str(rule),
                        'confidence': rule.confidence
                    })
        
        return explanations
    
    def _update_rule_statistics(self, rule_id: int, activation_strength: float) -> None:
        """Update usage statistics for a rule."""
        if rule_id in self.rule_statistics:
            stats = self.rule_statistics[rule_id]
            stats['activation_count'] += 1
            stats['total_activation_strength'] += activation_strength
            stats['average_activation_strength'] = (
                stats['total_activation_strength'] / stats['activation_count']
            )
    
    def _validate_rules(self) -> None:
        """Validate the rule base for consistency and completeness."""
        
        # Check for rule coverage
        consequent_terms = set()
        for rule in self.rules:
            consequent_terms.add(rule.consequent.linguistic_term)
        
        expected_terms = {'not_recommended', 'possibly_recommended', 'recommended', 'highly_recommended'}
        missing_terms = expected_terms - consequent_terms
        
        if missing_terms:
            print(f"Warning: No rules generate these consequents: {missing_terms}")
        
        # Check for conflicting rules (same antecedents, different consequents)
        antecedent_signatures = {}
        for rule in self.rules:
            signature = tuple(sorted(f"{ant.variable_name}:{ant.linguistic_term}" for ant in rule.antecedents))
            if signature in antecedent_signatures:
                existing_rule = antecedent_signatures[signature]
                if existing_rule.consequent.linguistic_term != rule.consequent.linguistic_term:
                    print(f"Warning: Conflicting rules detected - Rule {existing_rule.rule_id} and Rule {rule.rule_id}")
            else:
                antecedent_signatures[signature] = rule
    
    def print_rule_base(self) -> None:
        """Print the complete rule base in a readable format."""
        
        print("\n" + "="*80)
        print("FUZZY RULE BASE FOR MOVIE RECOMMENDATION SYSTEM")
        print("="*80)
        
        # Group rules by consequent for better organization
        rules_by_consequent = {}
        for rule in self.rules:
            consequent = rule.consequent.linguistic_term
            if consequent not in rules_by_consequent:
                rules_by_consequent[consequent] = []
            rules_by_consequent[consequent].append(rule)
        
        # Print rules organized by recommendation level
        order = ['highly_recommended', 'recommended', 'possibly_recommended', 'not_recommended']
        
        for consequent in order:
            if consequent in rules_by_consequent:
                print(f"\n{consequent.upper().replace('_', ' ')} RULES:")
                print("-" * 50)
                
                for rule in rules_by_consequent[consequent]:
                    print(f"\n{rule}")
                    print(f"  Confidence: {rule.confidence:.2f}")
                    print(f"  Description: {rule.description}")
        
        print(f"\nTotal Rules: {len(self.rules)}")
        print("="*80)
    
    def get_rule_statistics(self) -> Dict[int, Dict]:
        """Get usage statistics for all rules."""
        return self.rule_statistics.copy()


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the fuzzy rule engine.
    """
    
    print("Fuzzy Rule Engine for Movie Recommendation System")
    print("=" * 55)
    
    # Create rule engine and load rules
    rule_engine = FuzzyRuleEngine()
    rule_engine.create_movie_recommendation_rules()
    
    # Print complete rule base
    rule_engine.print_rule_base()
    
    # Test rule evaluation with sample input
    print("\nTesting Rule Evaluation:")
    print("-" * 30)
    
    # Sample input memberships
    sample_input = {
        'user_rating': {
            'low': 0.1,
            'medium': 0.3,
            'high': 0.8
        },
        'actor_popularity': {
            'unknown': 0.2,
            'known': 0.7,
            'famous': 0.4
        },
        'genre_match': {
            'poor': 0.1,
            'moderate': 0.2,
            'excellent': 0.9
        }
    }
    
    # Evaluate all rules
    activated_rules = rule_engine.evaluate_all_rules(sample_input)
    
    print("Activated Rules:")
    for consequent, rules in activated_rules.items():
        print(f"\n{consequent}:")
        for rule_id, strength in rules[:3]:  # Top 3 rules
            print(f"  Rule {rule_id}: Strength {strength:.3f}")
    
    # Get explanations
    explanations = rule_engine.get_rule_explanations(activated_rules, top_n=2)
    
    print("\nRule Explanations:")
    for consequent, explanations_list in explanations.items():
        print(f"\n{consequent}:")
        for explanation in explanations_list:
            print(f"  - {explanation['description']} (Strength: {explanation['strength']:.3f})")
