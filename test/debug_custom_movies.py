"""
Debug script to verify custom movies integration
"""
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from recommender.recommender_engine import MovieRecommendationEngine
from utils.data_loader import EnhancedDataLoader

print("=" * 70)
print("DEBUG: CUSTOM MOVIES INTEGRATION")
print("=" * 70)

# Step 1: Load custom movies CSV
print("\n1. Loading custom_movies.csv...")
custom_file = Path("data/custom_movies.csv")
if custom_file.exists():
    custom_df = pd.read_csv(custom_file)
    print(f"✓ Found {len(custom_df)} custom movies")
    print("\nCustom movies:")
    for idx, row in custom_df.iterrows():
        print(f"   - {row['title']}: {row['genres']} (Rating: {row['average_rating']})")
else:
    print("✗ custom_movies.csv not found!")
    sys.exit(1)

# Step 2: Generate sample dataset
print("\n2. Generating sample dataset...")
data_loader = EnhancedDataLoader(enable_caching=True)
movies_df = data_loader.create_sample_dataset(50)
print(f"✓ Generated {len(movies_df)} movies")

# Step 3: Merge custom movies
print("\n3. Merging custom movies with generated dataset...")
print(f"   Before merge: {len(movies_df)} movies")
movies_df = pd.concat([movies_df, custom_df], ignore_index=True)
print(f"   After merge: {len(movies_df)} movies")

# Step 4: Check if Nina is in merged dataset
print("\n4. Checking for 'Nina' in merged dataset...")
nina = movies_df[movies_df['title'] == 'Nina']
if len(nina) > 0:
    print("✓ 'Nina' found in merged dataset")
    print(f"   Title: {nina.iloc[0]['title']}")
    print(f"   Genres: {nina.iloc[0]['genres']}")
    print(f"   Rating: {nina.iloc[0]['average_rating']}")
else:
    print("✗ 'Nina' NOT found in merged dataset")

# Step 5: Initialize engine
print("\n5. Initializing recommendation engine...")
engine = MovieRecommendationEngine(defuzzification_method='centroid')
engine.initialize_system(movies_df)
print(f"✓ Engine initialized with {len(movies_df)} movies")

# Step 6: Check preprocessor database
print("\n6. Checking engine preprocessor database...")
if hasattr(engine, 'data_preprocessor'):
    db = engine.data_preprocessor.movie_database
    print(f"   Preprocessor has {len(db)} movies")
    
    nina_in_engine = db[db['title'] == 'Nina']
    if len(nina_in_engine) > 0:
        print("✓ 'Nina' found in engine database")
        print(f"   Title: {nina_in_engine.iloc[0]['title']}")
        print(f"   Genres: {nina_in_engine.iloc[0]['genres']}")
        print(f"   Rating: {nina_in_engine.iloc[0]['average_rating']}")
    else:
        print("✗ 'Nina' NOT found in engine database")
        print("\n   Available titles in engine:")
        for title in db['title'].head(10):
            print(f"      - {title}")
else:
    print("✗ Engine has no data_preprocessor")

# Step 7: Test recommendations for Thriller fan
print("\n7. Testing recommendations (Thriller preference)...")
print("   User preferences: Thriller only, min rating 9.0")

user_prefs = {
    'preferred_genres': ['Thriller'],
    'min_rating': 9.0,
    'preferred_actors': [],
    'preferred_directors': []
}

try:
    recommendations = engine.get_recommendations(
        user_preferences=user_prefs,
        num_recommendations=10
    )
    
    print(f"\n✓ Generated {len(recommendations)} recommendations")
    print("\n   Top 5 recommendations:")
    print("   " + "-" * 85)
    print(f"   {'#':<4} {'Title':<30} {'Score':<8} {'Rating':<8} {'Match%':<8} {'Genres':<20}")
    print("   " + "-" * 85)
    
    for idx, rec in enumerate(recommendations[:5], 1):
        match_pct = rec.get('genre_match_score', 0)
        genres = rec.get('genres', 'N/A')[:20]
        title = rec.get('title', 'N/A')
        score = rec.get('recommendation_score', 0)
        rating = rec.get('average_rating', 0)
        print(f"   {idx:<4} {title:<30} {score:<8.2f} {rating:<8.1f} {match_pct:<8.0f} {genres:<20}")
    
    # Check if Nina is in recommendations
    print("\n8. Checking if 'Nina' appears in recommendations...")
    nina_found = False
    nina_rank = 0
    for idx, rec in enumerate(recommendations, 1):
        if rec.get('title') == 'Nina':
            nina_found = True
            nina_rank = idx
            print(f"✓ 'Nina' found at rank #{nina_rank}")
            print(f"   Score: {rec.get('recommendation_score', 0):.2f}")
            print(f"   Match%: {rec.get('genre_match_score', 'N/A')}")
            break
    
    if not nina_found:
        print("✗ 'Nina' NOT in recommendations")
        print("\n   Analyzing why...")
        
        # Check Nina's data
        nina_data = movies_df[movies_df['title'] == 'Nina']
        if len(nina_data) > 0:
            print(f"   Nina's genres: '{nina_data.iloc[0]['genres']}'")
            print(f"   Nina's rating: {nina_data.iloc[0]['average_rating']}")
            print(f"   User wants: Thriller")
            print(f"   User min rating: 9.0")
            
            # Check if it's in the database at all
            if 'Nina' in db['title'].values:
                print("   ✓ Nina IS in engine database")
                nina_engine = db[db['title'] == 'Nina'].iloc[0]
                print(f"   Engine sees genres as: '{nina_engine['genres']}'")
            else:
                print("   ✗ Nina NOT in engine database (THIS IS THE PROBLEM!)")

except Exception as e:
    print(f"✗ Error generating recommendations: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)
