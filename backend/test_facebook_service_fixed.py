"""
Test the updated FacebookService with correct Pollinations URL
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.facebook_service import FacebookService
from dotenv import load_dotenv

load_dotenv()

async def test_poster_generation():
    """Test poster generation with the fixed service"""
    
    print("="*80)
    print("Testing FacebookService with fixed Pollinations URL")
    print("="*80)
    
    # Test data
    movie_data = {
        'movie_name': 'Leo 2',
        'hero_name': 'Vijay',
        'heroine_name': 'Trisha',
        'director_name': 'Lokesh Kanagaraj',
        'genre': 'action',
        'release_date': '2026-05-01',
        'requirements_poster': 'make the picture as hero is with a leopard walking in the snow and holding a hammer and make the text to be red'
    }
    
    service = FacebookService()
    
    # Check configuration
    print(f"\nConfiguration:")
    print(f"  Pollinations API Key: {'✓ Set' if service.pollinations_api_key else '✗ Not set'}")
    print(f"  Facebook Page ID: {'✓ Set' if service.page_id else '✗ Not set'}")
    print(f"  Facebook Token: {'✓ Set' if service.access_token else '✗ Not set'}")
    print(f"  Pollinations URL: {service.pollinations_base_url}")
    
    # Test 1: Build prompt
    print(f"\n{'='*80}")
    print("TEST 1: Build Prompt")
    print("="*80)
    prompt = service.build_poster_prompt(movie_data)
    print(f"Prompt (first 200 chars): {prompt[:200]}...")
    print(f"Full prompt length: {len(prompt)} characters")
    
    # Test 2: Generate caption
    print(f"\n{'='*80}")
    print("TEST 2: Generate Caption")
    print("="*80)
    caption = service.generate_caption(movie_data)
    print(f"Caption:\n{caption}")
    
    # Test 3: Generate poster
    print(f"\n{'='*80}")
    print("TEST 3: Generate Poster")
    print("="*80)
    poster_path = service.generate_and_save_poster(prompt, output_path="test_service_poster.png")
    
    if poster_path:
        file_size = Path(poster_path).stat().st_size
        print(f"\n✅ SUCCESS!")
        print(f"  Poster saved to: {poster_path}")
        print(f"  File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    else:
        print(f"\n❌ FAILED: Poster generation returned None")
    
    # Test 4: Full post creation (without actually posting to Facebook)
    print(f"\n{'='*80}")
    print("TEST 4: Full Post Creation Flow")
    print("="*80)
    
    result = await service.create_post(movie_data)
    
    print(f"\nResult:")
    print(f"  Success: {result.get('success')}")
    print(f"  Post ID: {result.get('post_id')}")
    print(f"  Mock: {result.get('mock', False)}")
    print(f"  Error: {result.get('error', 'None')}")
    
    if result.get('success'):
        print(f"\n✅ POST CREATION SUCCESSFUL!")
        if result.get('mock'):
            print(f"  (Mock mode - Facebook API not configured)")
        else:
            print(f"  Posted to Facebook!")
    else:
        print(f"\n❌ POST CREATION FAILED")
        print(f"  Error: {result.get('error')}")
    
    print(f"\n{'='*80}")
    print("ALL TESTS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_poster_generation())
