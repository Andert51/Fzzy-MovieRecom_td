"""
Simple test: Check if Nina appears in Thriller recommendations
"""
import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from recommender.recommender_engine import MovieRecommendationEngine
from utils.data_loader import EnhancedDataLoader

print("\n" + "="*70)
print("TESTING: Nina in Thriller Recommendations")
print("="*70 + "\n")

# Load data
print("1. Loading data...")
data_loader = EnhancedDataLoader(enable_caching=True)
movies_df = data_loader.create_sample_dataset(50)

# Load custom movies
custom_file = Path("data/custom_movies.csv")
custom_df = pd.read_csv(custom_file)

# IMPORTANT: Rename main_actors to actors if needed
if 'main_actors' in custom_df.columns:
    custom_df = custom_df.rename(columns={'main_actors': 'actors'})

# Merge
movies_df = pd.concat([movies_df, custom_df], ignore_index=True)
print(f"   Total movies: {len(movies_df)}")
print(f"   Custom movies: {len(custom_df)}")

# Initialize engine
print("\n2. Initializing engine...")
engine = MovieRecommendationEngine(defuzzification_method='centroid')
engine.initialize_system(movies_df)

# Check Nina is in database
db = engine.data_preprocessor.movie_database
nina_in_db = 'Nina' in db['title'].values
print(f"   Nina in database: {'✓ YES' if nina_in_db else '✗ NO'}")

# Generate recommendations for Thriller fan
print("\n3. Generating recommendations (Thriller, min rating 9.0)...")
user_prefs = {
    'preferred_genres': ['Thriller'],
    'min_rating': 9.0,
    'preferred_actors': [],
    'preferred_directors': []
}

recs = engine.get_recommendations(user_preferences=user_prefs, num_recommendations=10)

print(f"\n   Got {len(recs)} recommendations\n")
print("   " + "-"*90)
print(f"   {'#':<4} {'Title':<35} {'Score':<10} {'Rating':<10} {'Genres':<20}")
print("   " + "-"*90)

for i, rec in enumerate(recs[:10], 1):
    # rec is tuple: (movie_dict, score, explanation)
    movie_dict = rec[0]  # First element is the movie dictionary
    score = rec[1]       # Second is the recommendation score
    
    title = movie_dict.get('title', 'N/A')
    rating = movie_dict.get('average_rating', 0.0)
    genres = movie_dict.get('genres', 'N/A')
    
    marker = " ← NINA!" if title == "Nina" else ""
    print(f"   {i:<4} {title:<35} {score:<10.2f} {rating:<10.1f} {genres:<20}{marker}")

print("   " + "-"*90)

# Check if Nina is #1
if len(recs) > 0 and recs[0][0].get('title') == 'Nina':
    print("\n✅ SUCCESS: Nina is the #1 recommendation!")
    print(f"   Score: {recs[0][1]:.2f}")
    print(f"   Rating: {recs[0][0].get('average_rating')}")
    print(f"   Genres: {recs[0][0].get('genres')}")
elif any(r[0].get('title') == 'Nina' for r in recs):
    nina_pos = next(i for i, r in enumerate(recs, 1) if r[0].get('title') == 'Nina')
    print(f"\n⚠️  Nina appears at position #{nina_pos} (not #1)")
    nina_rec = recs[nina_pos - 1]
    print(f"   Score: {nina_rec[1]:.2f}")
    print(f"   Rating: {nina_rec[0].get('average_rating')}")
else:
    print("\n❌ FAIL: Nina not in recommendations")

print("\n" + "="*70 + "\n")
