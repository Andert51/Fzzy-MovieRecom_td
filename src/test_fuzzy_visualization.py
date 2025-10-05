"""
Quick test for fuzzy membership visualization features
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import ModernFuzzyApp

print("\n" + "="*70)
print("TESTING: Fuzzy Membership Visualization Features")
print("="*70 + "\n")

# Initialize app
app = ModernFuzzyApp()
app.initialize_system(num_movies=50, verbose=True)

print("\n1. Testing fuzzy label calculation...")
test_scores = [95, 85, 70, 55, 35, 15]
for score in test_scores:
    label, visual = app._get_fuzzy_label(score)
    print(f"   Score {score:3.0f} → {visual} ({label})")

print("\n2. Generating recommendations for Thriller fan...")
user_prefs = {
    'preferred_genres': ['Thriller'],
    'min_rating': 9.0,
    'preferred_actors': [],
    'preferred_directors': []
}

recommendations = app.engine.get_recommendations(
    user_preferences=user_prefs,
    num_recommendations=5
)

print(f"\n   Got {len(recommendations)} recommendations")

# Display with fuzzy labels
print("\n   " + "-"*85)
print(f"   {'#':<4} {'Title':<30} {'Score':<10} {'Fuzzy':<8} {'Label':<20}")
print("   " + "-"*85)

for i, (movie, score, _) in enumerate(recommendations, 1):
    label, visual = app._get_fuzzy_label(score)
    title = movie['title'][:28]
    print(f"   {i:<4} {title:<30} {score:<10.2f} {visual:<8} {label:<20}")

print("\n3. Generating membership function visualization...")
membership_path = app._plot_membership_with_scores(recommendations)

if membership_path:
    print(f"   ✅ SUCCESS: Saved to {membership_path}")
else:
    print("   ❌ FAIL: Could not generate membership plot")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70 + "\n")
