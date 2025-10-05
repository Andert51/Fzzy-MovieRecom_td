"""
Quick test script to validate the fixes for genre preference handling.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from recommender.recommender_engine import MovieRecommendationEngine

print("=" * 70)
print("TESTING GENRE PREFERENCE FIXES")
print("=" * 70)

# Initialize engine
print("\n1. Initializing system...")
engine = MovieRecommendationEngine()

# Create sample data
sample_movies = pd.DataFrame([
    {
        'movie_id': 'movie_001',
        'title': 'The Funny Side',
        'genres': 'Comedy|Romance',
        'actors': 'Jim Carrey|Cameron Diaz',
        'director': 'Director A',
        'average_rating': 9.5,
        'release_year': 2020
    },
    {
        'movie_id': 'movie_002',
        'title': 'Edge of Tomorrow',
        'genres': 'Thriller|Sci-Fi',
        'actors': 'Tom Cruise|Emily Blunt',
        'director': 'Director B',
        'average_rating': 9.9,
        'release_year': 2014
    },
    {
        'movie_id': 'movie_003',
        'title': 'Mad House',
        'genres': 'Comedy|Family',
        'actors': 'Adam Sandler|Drew Barrymore',
        'director': 'Director C',
        'average_rating': 9.2,
        'release_year': 2018
    },
    {
        'movie_id': 'movie_004',
        'title': 'Nightmare House',
        'genres': 'Horror',
        'actors': 'Unknown',
        'director': 'Director D',
        'average_rating': 9.9,
        'release_year': 2019
    },
    {
        'movie_id': 'movie_005',
        'title': 'Comedy Gold',
        'genres': 'Comedy',
        'actors': 'Chris Rock|Kevin Hart',
        'director': 'Director E',
        'average_rating': 9.8,
        'release_year': 2021
    }
])

engine.initialize_system(sample_movies)
print("✓ System initialized with 5 movies")

# Test with Comedy preference
print("\n2. Creating user with Comedy preference...")
user_prefs = {
    'preferred_genres': ['Comedy'],
    'favorite_actors': [],
    'min_rating': 9.0
}

print(f"   Preferred genres: {user_prefs['preferred_genres']}")
print(f"   Min rating: {user_prefs['min_rating']}")

# Get recommendations
print("\n3. Generating recommendations...")
try:
    recommendations = engine.get_recommendations(
        user_preferences=user_prefs,
        num_recommendations=5
    )
    
    print(f"✓ Generated {len(recommendations)} recommendations")
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS:")
    print("=" * 70)
    print(f"{'Rank':<6} {'Title':<25} {'Score':<10} {'Rating':<10} {'Match%':<10} {'Genres':<20}")
    print("-" * 70)
    
    for i, (movie, score, explanation) in enumerate(recommendations, 1):
        title = movie['title'][:24]
        rating = movie.get('average_rating', 0)
        genres = movie.get('genres', 'N/A')[:19]
        match = movie.get('genre_match_score', 0)
        
        print(f"{i:<6} {title:<25} {score:<10.1f} {rating:<10.1f} {match:<10.0f} {genres:<20}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    
    # Check if Comedy movies are prioritized
    comedy_ranks = []
    non_comedy_ranks = []
    
    for i, (movie, score, _) in enumerate(recommendations, 1):
        genres = movie.get('genres', '')
        if 'Comedy' in genres:
            comedy_ranks.append((i, movie['title'], score))
        else:
            non_comedy_ranks.append((i, movie['title'], score))
    
    print(f"\nComedy movies (should be first):")
    for rank, title, score in comedy_ranks:
        print(f"  Rank {rank}: {title} (Score: {score:.1f})")
    
    print(f"\nNon-Comedy movies (should be last):")
    for rank, title, score in non_comedy_ranks:
        print(f"  Rank {rank}: {title} (Score: {score:.1f})")
    
    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT:")
    print("=" * 70)
    
    if comedy_ranks and comedy_ranks[0][0] == 1:
        print("✅ SUCCESS: Comedy movie is ranked #1")
    else:
        print("❌ FAIL: Comedy movie is NOT ranked #1")
    
    if len(comedy_ranks) >= 2 and all(r[0] <= len(comedy_ranks) for r in comedy_ranks):
        print("✅ SUCCESS: All Comedy movies are in top positions")
    else:
        print("⚠️  WARNING: Some Comedy movies are ranked low")
    
    # Check genre_match_score exposure
    first_movie = recommendations[0][0]
    if 'genre_match_score' in first_movie:
        print(f"✅ SUCCESS: genre_match_score is exposed (value: {first_movie['genre_match_score']:.0f})")
    else:
        print("❌ FAIL: genre_match_score is NOT exposed")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
