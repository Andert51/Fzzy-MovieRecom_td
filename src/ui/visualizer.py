"""
Fuzzy Logic Visualizer

Creates professional visualizations for fuzzy logic components:
- Membership functions
- Fuzzy inference process
- Recommendation analysis
- Data statistics
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Set professional style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['grid.alpha'] = 0.3


class FuzzyVisualizer:
    """
    Professional visualizer for fuzzy logic movie recommendation system.
    
    Generates clear, publication-quality plots for:
    - Membership functions
    - Fuzzy variables
    - Inference results
    - Data analysis
    """
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Professional color scheme
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#06A77D',
            'warning': '#F77F00',
            'danger': '#D62828',
            'info': '#4ECDC4',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
    
    def plot_membership_functions(self, 
                                  fuzzy_variables, 
                                  save_name: str = "membership_functions.png",
                                  show: bool = False) -> str:
        """
        Visualize all membership functions in a 2x2 grid.
        
        Args:
            fuzzy_variables: FuzzyVariables object
            save_name: Filename for saved plot
            show: Whether to display plot
            
        Returns:
            Path to saved plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Fuzzy Logic Membership Functions', 
                     fontsize=18, fontweight='bold', y=0.995)
        
        # User Rating
        ax = axes[0, 0]
        for term in ['low', 'medium', 'high']:
            mf = fuzzy_variables.user_rating[term].mf
            ax.plot(fuzzy_variables.user_rating.universe, mf, 
                   linewidth=2.5, label=term.title(), alpha=0.8)
        ax.set_title('User Rating', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Rating (1-10)', fontsize=11)
        ax.set_ylabel('Membership Degree', fontsize=11)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
        # Actor Popularity
        ax = axes[0, 1]
        for term in ['unknown', 'known', 'famous']:
            mf = fuzzy_variables.actor_popularity[term].mf
            ax.plot(fuzzy_variables.actor_popularity.universe, mf, 
                   linewidth=2.5, label=term.title(), alpha=0.8)
        ax.set_title('Actor Popularity', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Popularity Score (0-100)', fontsize=11)
        ax.set_ylabel('Membership Degree', fontsize=11)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
        # Genre Match
        ax = axes[1, 0]
        for term in ['poor', 'moderate', 'excellent']:
            mf = fuzzy_variables.genre_match[term].mf
            ax.plot(fuzzy_variables.genre_match.universe, mf, 
                   linewidth=2.5, label=term.title(), alpha=0.8)
        ax.set_title('Genre Match', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Match Percentage (0-100)', fontsize=11)
        ax.set_ylabel('Membership Degree', fontsize=11)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
        # Recommendation Output
        ax = axes[1, 1]
        for term in ['not_recommended', 'possibly_recommended', 'recommended', 'highly_recommended']:
            mf = fuzzy_variables.recommendation[term].mf
            ax.plot(fuzzy_variables.recommendation.universe, mf, 
                   linewidth=2.5, label=term.replace('_', ' ').title(), alpha=0.8)
        ax.set_title('Recommendation Score', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Score (0-100)', fontsize=11)
        ax.set_ylabel('Membership Degree', fontsize=11)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        
        plt.tight_layout()
        
        save_path = self.output_dir / save_name
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(save_path)
    
    def plot_fuzzy_inference(self,
                            input_values: Dict[str, float],
                            output_value: float,
                            fuzzy_variables,
                            activated_rules: Optional[List] = None,
                            save_name: str = "fuzzy_inference.png",
                            show: bool = False) -> str:
        """
        Visualize the fuzzy inference process for given inputs.
        
        Args:
            input_values: Dict with 'user_rating', 'actor_popularity', 'genre_match'
            output_value: Computed recommendation score
            fuzzy_variables: FuzzyVariables object
            activated_rules: List of activated rules
            save_name: Filename for saved plot
            show: Whether to display plot
            
        Returns:
            Path to saved plot
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle('Fuzzy Inference Process', 
                     fontsize=18, fontweight='bold', y=0.98)
        
        # Input 1: User Rating
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_input_activation(ax1, fuzzy_variables.user_rating,
                                    input_values['user_rating'], 'User Rating')
        
        # Input 2: Actor Popularity
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_input_activation(ax2, fuzzy_variables.actor_popularity,
                                    input_values['actor_popularity'], 'Actor Popularity')
        
        # Input 3: Genre Match
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_input_activation(ax3, fuzzy_variables.genre_match,
                                    input_values['genre_match'], 'Genre Match')
        
        # Output: Recommendation
        ax4 = fig.add_subplot(gs[1, :])
        self._plot_output_activation(ax4, fuzzy_variables.recommendation,
                                     output_value, 'Recommendation Score')
        
        # Rules activation (if provided)
        if activated_rules:
            ax5 = fig.add_subplot(gs[2, :])
            self._plot_rule_activation(ax5, activated_rules)
        else:
            # Show input-output summary
            ax5 = fig.add_subplot(gs[2, :])
            self._plot_io_summary(ax5, input_values, output_value)
        
        plt.tight_layout()
        
        save_path = self.output_dir / save_name
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(save_path)
    
    def _plot_input_activation(self, ax, variable, value, title):
        """Helper to plot input variable activation."""
        for term in variable.terms:
            mf = variable[term].mf
            ax.plot(variable.universe, mf, linewidth=2, alpha=0.6, label=term)
        
        # Mark the input value
        ax.axvline(value, color=self.colors['danger'], linewidth=2.5, 
                  linestyle='--', label=f'Input: {value:.1f}')
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_ylabel('Membership', fontsize=10)
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
    
    def _plot_output_activation(self, ax, variable, value, title):
        """Helper to plot output variable activation."""
        for term in variable.terms:
            mf = variable[term].mf
            ax.plot(variable.universe, mf, linewidth=2, alpha=0.6, label=term.replace('_', ' ').title())
        
        # Mark the output value
        ax.axvline(value, color=self.colors['success'], linewidth=3, 
                  linestyle='--', label=f'Output: {value:.2f}')
        ax.axvspan(max(0, value-5), min(100, value+5), alpha=0.2, color=self.colors['success'])
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Score', fontsize=10)
        ax.set_ylabel('Membership', fontsize=10)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
    
    def _plot_rule_activation(self, ax, rules):
        """Helper to plot activated rules."""
        rule_names = [f"Rule {i+1}" for i in range(min(len(rules), 10))]
        activations = [rule.get('activation', 0) for rule in rules[:10]]
        
        bars = ax.barh(rule_names, activations, color=self.colors['primary'], alpha=0.7)
        
        # Color bars by activation level
        for i, (bar, act) in enumerate(zip(bars, activations)):
            if act > 0.7:
                bar.set_color(self.colors['success'])
            elif act > 0.4:
                bar.set_color(self.colors['warning'])
            else:
                bar.set_color(self.colors['info'])
        
        ax.set_xlabel('Activation Level', fontsize=10)
        ax.set_title('Rule Firing Strength', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.grid(True, alpha=0.3, axis='x')
    
    def _plot_io_summary(self, ax, inputs, output):
        """Helper to plot input-output summary."""
        ax.axis('off')
        
        summary_text = f"""
        INPUT VALUES
        ─────────────────────────────
        User Rating:        {inputs['user_rating']:.2f}
        Actor Popularity:   {inputs['actor_popularity']:.2f}
        Genre Match:        {inputs['genre_match']:.2f}
        
        OUTPUT RESULT
        ─────────────────────────────
        Recommendation Score: {output:.2f}/100
        
        INTERPRETATION
        ─────────────────────────────
        {self._get_interpretation(output)}
        """
        
        ax.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
               verticalalignment='center', bbox=dict(boxstyle='round', 
               facecolor=self.colors['light'], alpha=0.8, pad=1))
    
    def _get_interpretation(self, score):
        """Get linguistic interpretation of score."""
        if score >= 80:
            return "Status: HIGHLY RECOMMENDED\n        This movie is an excellent match!"
        elif score >= 60:
            return "Status: RECOMMENDED\n        This movie is a good choice."
        elif score >= 40:
            return "Status: POSSIBLY RECOMMENDED\n        This movie might be worth watching."
        else:
            return "Status: NOT RECOMMENDED\n        This movie may not suit your preferences."
    
    def plot_recommendations(self,
                           recommendations: List[Dict],
                           save_name: str = "recommendations.png",
                           show: bool = False) -> str:
        """
        Visualize recommendation results.
        
        Args:
            recommendations: List of recommendation dicts with movie info and scores
            save_name: Filename for saved plot
            show: Whether to display plot
            
        Returns:
            Path to saved plot
        """
        if not recommendations:
            return None
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle('Movie Recommendations Analysis', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Extract data
        titles = [rec['title'][:30] for rec in recommendations[:10]]
        scores = [rec['score'] for rec in recommendations[:10]]
        ratings = [rec.get('average_rating', 0) for rec in recommendations[:10]]
        
        # Plot 1: Recommendation scores
        ax1 = axes[0]
        bars = ax1.barh(titles, scores, color=self.colors['primary'], alpha=0.7)
        
        # Color bars by score
        for bar, score in zip(bars, scores):
            if score >= 80:
                bar.set_color(self.colors['success'])
            elif score >= 60:
                bar.set_color(self.colors['info'])
            elif score >= 40:
                bar.set_color(self.colors['warning'])
            else:
                bar.set_color(self.colors['danger'])
        
        ax1.set_xlabel('Recommendation Score', fontsize=11)
        ax1.set_title('Top Recommendations by Fuzzy Score', fontsize=13, fontweight='bold', pad=15)
        ax1.set_xlim(0, 100)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Add score labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax1.text(score + 1, i, f'{score:.1f}', va='center', fontsize=9)
        
        # Plot 2: Score vs Rating comparison
        ax2 = axes[1]
        x = np.arange(len(titles))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, scores, width, label='Fuzzy Score', 
                       color=self.colors['primary'], alpha=0.7)
        bars2 = ax2.bar(x + width/2, [r*10 for r in ratings], width, 
                       label='Movie Rating (×10)', color=self.colors['accent'], alpha=0.7)
        
        ax2.set_xlabel('Movies', fontsize=11)
        ax2.set_ylabel('Score', fontsize=11)
        ax2.set_title('Fuzzy Score vs Movie Rating Comparison', fontsize=13, fontweight='bold', pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels(titles, rotation=45, ha='right', fontsize=9)
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        
        save_path = self.output_dir / save_name
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(save_path)
    
    def plot_data_statistics(self,
                            movies_df: pd.DataFrame,
                            save_name: str = "data_statistics.png",
                            show: bool = False) -> str:
        """
        Visualize movie dataset statistics.
        
        Args:
            movies_df: DataFrame with movie data
            save_name: Filename for saved plot
            show: Whether to display plot
            
        Returns:
            Path to saved plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Movie Dataset Analysis', 
                     fontsize=18, fontweight='bold', y=0.995)
        
        # 1. Rating distribution
        ax1 = axes[0, 0]
        sns.histplot(movies_df['average_rating'], bins=20, kde=True, 
                    color=self.colors['primary'], ax=ax1, alpha=0.7)
        ax1.set_title('Rating Distribution', fontsize=13, fontweight='bold', pad=15)
        ax1.set_xlabel('Average Rating', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        # 2. Genre distribution
        ax2 = axes[0, 1]
        all_genres = []
        for genres in movies_df['genres']:
            if isinstance(genres, str):
                all_genres.extend(genres.split('|'))
        
        genre_counts = pd.Series(all_genres).value_counts().head(8)
        genre_counts.plot(kind='barh', ax=ax2, color=self.colors['accent'], alpha=0.7)
        ax2.set_title('Top Genres', fontsize=13, fontweight='bold', pad=15)
        ax2.set_xlabel('Number of Movies', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Release year distribution
        ax3 = axes[1, 0]
        if 'release_year' in movies_df.columns:
            year_counts = movies_df['release_year'].value_counts().sort_index()
            ax3.plot(year_counts.index, year_counts.values, 
                    marker='o', linewidth=2, markersize=4, 
                    color=self.colors['success'], alpha=0.7)
            ax3.fill_between(year_counts.index, year_counts.values, alpha=0.3, 
                           color=self.colors['success'])
            ax3.set_title('Movies by Release Year', fontsize=13, fontweight='bold', pad=15)
            ax3.set_xlabel('Year', fontsize=11)
            ax3.set_ylabel('Number of Movies', fontsize=11)
            ax3.grid(True, alpha=0.3)
        
        # 4. Rating vs Year
        ax4 = axes[1, 1]
        if 'release_year' in movies_df.columns:
            scatter = ax4.scatter(movies_df['release_year'], 
                                 movies_df['average_rating'],
                                 c=movies_df['average_rating'], 
                                 cmap='RdYlGn', s=50, alpha=0.6)
            ax4.set_title('Rating vs Release Year', fontsize=13, fontweight='bold', pad=15)
            ax4.set_xlabel('Release Year', fontsize=11)
            ax4.set_ylabel('Average Rating', fontsize=11)
            ax4.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax4, label='Rating')
        
        plt.tight_layout()
        
        save_path = self.output_dir / save_name
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(save_path)
    
    def create_dashboard(self,
                        fuzzy_variables,
                        movies_df: pd.DataFrame,
                        sample_inference: Optional[Dict] = None,
                        save_name: str = "dashboard.png",
                        show: bool = False) -> str:
        """
        Create a comprehensive dashboard with all visualizations.
        
        Args:
            fuzzy_variables: FuzzyVariables object
            movies_df: DataFrame with movie data
            sample_inference: Optional dict with sample inference data
            save_name: Filename for saved plot
            show: Whether to display plot
            
        Returns:
            Path to saved plot
        """
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        fig.suptitle('Fuzzy Logic Movie Recommendation System - Dashboard', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # System info
        ax_info = fig.add_subplot(gs[0, 0])
        ax_info.axis('off')
        info_text = f"""
        SYSTEM INFORMATION
        ══════════════════════════════
        
        Fuzzy Variables:  4
        Membership Funcs: 16
        Fuzzy Rules:      15
        Inference Method: Mamdani
        
        Dataset Size:     {len(movies_df)}
        Avg Rating:       {movies_df['average_rating'].mean():.2f}
        Rating Range:     {movies_df['average_rating'].min():.1f} - {movies_df['average_rating'].max():.1f}
        """
        ax_info.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                    verticalalignment='center', bbox=dict(boxstyle='round',
                    facecolor=self.colors['light'], alpha=0.9, pad=1))
        ax_info.set_title('System Overview', fontsize=12, fontweight='bold', pad=10)
        
        # Membership function samples (2 variables)
        ax_mf1 = fig.add_subplot(gs[0, 1])
        for term in fuzzy_variables.user_rating.terms:
            mf = fuzzy_variables.user_rating[term].mf
            ax_mf1.plot(fuzzy_variables.user_rating.universe, mf, linewidth=2, alpha=0.7, label=term)
        ax_mf1.set_title('User Rating MF', fontsize=11, fontweight='bold')
        ax_mf1.set_ylabel('Membership', fontsize=9)
        ax_mf1.legend(fontsize=7, loc='best')
        ax_mf1.grid(True, alpha=0.3)
        ax_mf1.set_ylim(-0.05, 1.05)
        
        ax_mf2 = fig.add_subplot(gs[0, 2])
        for term in fuzzy_variables.recommendation.terms:
            mf = fuzzy_variables.recommendation[term].mf
            ax_mf2.plot(fuzzy_variables.recommendation.universe, mf, linewidth=2, alpha=0.7,
                       label=term.replace('_', ' '))
        ax_mf2.set_title('Recommendation Output MF', fontsize=11, fontweight='bold')
        ax_mf2.set_ylabel('Membership', fontsize=9)
        ax_mf2.legend(fontsize=7, loc='best')
        ax_mf2.grid(True, alpha=0.3)
        ax_mf2.set_ylim(-0.05, 1.05)
        
        # Data statistics
        ax_rating = fig.add_subplot(gs[1, 0])
        sns.histplot(movies_df['average_rating'], bins=15, kde=True,
                    color=self.colors['primary'], ax=ax_rating, alpha=0.7)
        ax_rating.set_title('Rating Distribution', fontsize=11, fontweight='bold')
        ax_rating.set_xlabel('Rating', fontsize=9)
        ax_rating.set_ylabel('Count', fontsize=9)
        ax_rating.grid(True, alpha=0.3)
        
        ax_genre = fig.add_subplot(gs[1, 1:])
        all_genres = []
        for genres in movies_df['genres']:
            if isinstance(genres, str):
                all_genres.extend(genres.split('|'))
        genre_counts = pd.Series(all_genres).value_counts().head(10)
        genre_counts.plot(kind='barh', ax=ax_genre, color=self.colors['accent'], alpha=0.7)
        ax_genre.set_title('Top 10 Genres', fontsize=11, fontweight='bold')
        ax_genre.set_xlabel('Count', fontsize=9)
        ax_genre.grid(True, alpha=0.3, axis='x')
        
        # Sample inference (if provided)
        if sample_inference:
            ax_inference = fig.add_subplot(gs[2, :])
            inputs = sample_inference.get('inputs', {})
            output = sample_inference.get('output', 0)
            
            # Bar chart showing inputs and output
            labels = ['User\nRating', 'Actor\nPopularity', 'Genre\nMatch', 'Output\nScore']
            values = [
                inputs.get('user_rating', 0) * 10,  # Normalize to 0-100
                inputs.get('actor_popularity', 0),
                inputs.get('genre_match', 0),
                output
            ]
            colors_list = [self.colors['info'], self.colors['info'], 
                          self.colors['info'], self.colors['success']]
            
            bars = ax_inference.bar(labels, values, color=colors_list, alpha=0.7)
            ax_inference.set_ylabel('Score', fontsize=10)
            ax_inference.set_title('Sample Fuzzy Inference', fontsize=12, fontweight='bold', pad=15)
            ax_inference.set_ylim(0, 100)
            ax_inference.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax_inference.text(bar.get_x() + bar.get_width()/2., height + 1,
                                f'{val:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        save_path = self.output_dir / save_name
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return str(save_path)
