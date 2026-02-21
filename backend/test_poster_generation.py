"""
Test Poster Generation
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.facebook_service import FacebookService

async def test_poster_generation():
    """Test poster generation with different methods"""
    
    print("=" * 70)
    print("Poster Generation Test")
    print("=" * 70)
    
    fb_service = FacebookService()
    
    # Test movie data
    movie_data = {
        'movie_name': 'Leo 2',
        'hero_name': 'Vijay',
        'heroine_name': 'Trisha',
        'director_name': 'Lokesh Kanagaraj',
        'genre': 'action',
        'release_date': '2026-05-01',
        'requirements_poster': 'make the picture as hero is with a leopard walking in the snow and holding a hammer and make the text to be red'
    }
    
    print(f"\n1. Building prompt for '{movie_data['movie_name']}'...")
    prompt = fb_service.build_poster_prompt(movie_data)
    
    print(f"\nPrompt: {prompt}")
    print(f"\nPrompt length: {len(prompt)} characters")
    
    print(f"\n2. Generating poster...")
    poster_path = fb_service.generate_and_save_poster(prompt, output_path="test_poster.png")
    
    if poster_path:
        print(f"\n✅ SUCCESS! Poster saved to: {poster_path}")
        
        # Check file size
        import os
        file_size = os.path.getsize(poster_path)
        print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        if file_size > 10000:
            print("✅ File size looks good (>10KB)")
        else:
            print("⚠️ File size is very small, might be an error page")
    else:
        print(f"\n❌ FAILED: Could not generate poster")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_poster_generation())
