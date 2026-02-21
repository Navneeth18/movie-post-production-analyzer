"""
Test Complete Facebook Campaign Flow with Image Generation
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.facebook_service import FacebookService
from datetime import datetime

async def test_complete_flow():
    """Test the complete flow: generate content, generate image, post to Facebook"""
    
    print("=" * 70)
    print("Complete Facebook Campaign Flow Test")
    print("=" * 70)
    
    fb_service = FacebookService()
    
    # Test movie data
    movie_data = {
        'title': 'Test Movie',
        'director': 'Test Director',
        'genres': ['Action', 'Drama'],
        'release_date': datetime(2026, 12, 25),
        'cast': [
            {'name': 'Actor 1', 'role': 'Hero'},
            {'name': 'Actor 2', 'role': 'Heroine'}
        ]
    }
    
    campaign_type = 'teaser'
    
    print(f"\n1. Generating campaign content for '{movie_data['title']}'...")
    print(f"   Campaign Type: {campaign_type}")
    
    # Generate content
    content = fb_service.generate_campaign_content(movie_data, campaign_type)
    
    print(f"\n   ✅ Content generated:")
    print(f"   Message: {content['message'][:100]}...")
    print(f"   Hashtags: {', '.join(content['hashtags'][:3])}")
    print(f"   Image Prompt: {content['image_prompt'][:100]}...")
    
    print(f"\n2. Generating AI image...")
    image_url = await fb_service.generate_image_with_pollinations(content['image_prompt'])
    
    if image_url:
        print(f"   ✅ Image URL: {image_url}")
    else:
        print(f"   ⚠️  Image generation unavailable, will post without image")
    
    print(f"\n3. Creating Facebook post...")
    result = await fb_service.create_post(
        message=content['message'],
        image_url=None,  # Let it auto-generate
        auto_generate_image=True,
        image_prompt=content['image_prompt']
    )
    
    if result['success']:
        print(f"   ✅ Post created successfully!")
        print(f"   Post ID: {result['post_id']}")
        print(f"   Mock Mode: {result.get('mock', False)}")
        
        if result.get('image_url'):
            print(f"   Image attached: Yes")
        else:
            print(f"   Image attached: No (text-only post)")
        
        if not result.get('mock'):
            print(f"\n   🎉 Check your Facebook page to see the post!")
            
            # Ask if user wants to delete the test post
            print(f"\n   Note: This is a test post. You may want to delete it from your page.")
    else:
        print(f"   ❌ Post creation failed")
        print(f"   Error: {result.get('error')}")
        print(f"   Error Code: {result.get('error_code')}")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_complete_flow())
