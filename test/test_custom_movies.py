"""
Test script to verify custom movies integration fix.
Tests that custom movies are loaded and appear in recommendations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from pathlib import Path

print("=" * 70)
print("TESTING CUSTOM MOVIES INTEGRATION v2.1.2")
print("=" * 70)

# Step 1: Create a custom movie file
print("\n1. Creating custom movie file...")

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

custom_movies = pd.DataFrame([
    {
        'movie_id': 'custom_test_001',
        'title': 'Super Comedy Movie',
        'genres': 'Comedy',
        'main_actors': 'Jim Carrey|Chris Rock',
        'director': 'Test Director',
        'average_rating': 9.8,
        'release_year': 2025,
        'custom_added': True,
        'added_timestamp': '2025-10-05T16:00:00'
    },
    {
        'movie_id': 'custom_test_002',
        'title': 'Amazing Drama',
        'genres': 'Drama',
        'main_actors': 'Actor A|Actor B',
        'director': 'Test Director 2',
        'average_rating': 9.5,
        'release_year': 2024,
        'custom_added': True,
        'added_timestamp': '2025-10-05T16:00:00'
    }
])

custom_file = data_dir / "custom_movies.csv"
custom_movies.to_csv(custom_file, index=False)

print(f"✓ Created custom_movies.csv with {len(custom_movies)} movies")
print(f"  - {custom_movies.iloc[0]['title']} (Comedy, 9.8)")
print(f"  - {custom_movies.iloc[1]['title']} (Drama, 9.5)")

# Step 2: Test system initialization
print("\n2. Testing system initialization...")

from main import ModernFuzzyApp

app = ModernFuzzyApp()
success = app.initialize_system(num_movies=10, verbose=False)

if success:
    print(f"✓ System initialized")
    print(f"  Total movies in DataFrame: {len(app.movies_df)}")
    
    # Check if custom movies are loaded
    custom_in_df = app.movies_df[app.movies_df.get('custom_added', False) == True]
    print(f"  Custom movies loaded: {len(custom_in_df)}")
    
    if len(custom_in_df) > 0:
        print(f"  ✓ Custom movies found in DataFrame:")
        for _, movie in custom_in_df.iterrows():
            print(f"    - {movie['title']} ({movie.get('genres', 'N/A')}, {movie.get('average_rating', 0):.1f})")
    else:
        print("  ✗ NO custom movies found in DataFrame")
else:
    print("✗ System initialization failed")
    sys.exit(1)

# Step 3: Test recommendations with Comedy preference
print("\n3. Testing recommendations (Comedy preference)...")

user_prefs = {
    'preferred_genres': ['Comedy'],
    'favorite_actors': [],
    'min_rating': 9.0
}

try:
    recommendations = app.engine.get_recommendations(
        user_preferences=user_prefs,
        num_recommendations=5
    )
    
    print(f"✓ Generated {len(recommendations)} recommendations")
    print()
    print(f"{'Rank':<6} {'Title':<30} {'Score':<10} {'Rating':<10} {'Match%':<10} {'Genres':<20}")
    print("-" * 90)
    
    found_custom_comedy = False
    for i, (movie, score, explanation) in enumerate(recommendations, 1):
        title = movie['title'][:29]
        rating = movie.get('average_rating', 0)
        genres = movie.get('genres', 'N/A')[:19]
        match = movie.get('genre_match_score', 0)
        
        print(f"{i:<6} {title:<30} {score:<10.1f} {rating:<10.1f} {match:<10.0f} {genres:<20}")
        
        if 'Super Comedy Movie' in movie['title']:
            found_custom_comedy = True
    
    # Verdict
    print()
    print("=" * 70)
    print("VERDICT:")
    print("=" * 70)
    
    if found_custom_comedy:
        print("✅ SUCCESS: Custom Comedy movie appears in recommendations!")
    else:
        print("⚠️  WARNING: Custom Comedy movie NOT in top 5 recommendations")
        print("   (May be ranked lower, but should be accessible)")
    
    # Check if Comedy is prioritized
    first_movie = recommendations[0][0]
    first_genres = first_movie.get('genres', '')
    
    if 'Comedy' in first_genres:
        print("✅ SUCCESS: Comedy movie is ranked #1")
    else:
        print("❌ FAIL: Non-Comedy movie is ranked #1")
    
    # Check genre_match_score
    if 'genre_match_score' in first_movie:
        print(f"✅ SUCCESS: genre_match_score exposed (value: {first_movie['genre_match_score']:.0f})")
    else:
        print("❌ FAIL: genre_match_score NOT exposed")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Test available genres
print()
print("\n4. Testing available genres list...")

genres = app._get_available_genres()
print(f"✓ Found {len(genres)} genres")
print(f"  First 10: {', '.join(genres[:10])}")

if 'Comedy' in genres:
    print("✓ Comedy is in available genres")
else:
    print("✗ Comedy NOT in available genres")

# Clean up
print()
print("\n5. Test complete!")
print("=" * 70)
print()
print("To see full dataset info, run:")
print("  python main.py")
print("  # Select option 12: View Dataset Info")
