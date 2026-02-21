"""
Test Pollinations AI Image Generation
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.facebook_service import FacebookService

async def test_image_generation():
    """Test image generation with Pollinations"""
    
    print("=" * 70)
    print("Pollinations AI Image Generation Test")
    print("=" * 70)
    
    fb_service = FacebookService()
    
    # Test different campaign types
    test_cases = [
        {
            'title': 'Baahubali 3',
            'director': 'SS Rajamouli',
            'genres': ['Action', 'Drama'],
            'campaign_type': 'teaser'
        },
        {
            'title': 'RRR 2',
            'director': 'SS Rajamouli',
            'genres': ['Action', 'Historical'],
            'campaign_type': 'trailer'
        },
        {
            'title': 'Pushpa 3',
            'director': 'Sukumar',
            'genres': ['Action', 'Thriller'],
            'campaign_type': 'release'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['campaign_type'].upper()} for '{test_case['title']}'")
        print("-" * 70)
        
        # Generate prompt
        prompt = fb_service.generate_image_prompt(test_case, test_case['campaign_type'])
        print(f"Prompt: {prompt}")
        
        # Generate image
        print("\nGenerating image...")
        image_url = await fb_service.generate_image_with_pollinations(prompt)
        
        if image_url:
            print(f"✅ Success! Image URL: {image_url}")
            print(f"\nYou can view the image at: {image_url}")
        else:
            print("❌ Failed to generate image")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print("\nNote: The generated images are accessible via the URLs above.")
    print("You can use these URLs directly in Facebook posts.")

if __name__ == "__main__":
    asyncio.run(test_image_generation())
