"""
Test Pollinations API directly with the exact URL from working script
"""
import os
import requests
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Test data
prompt = "Create a cinematic action movie poster for the film 'Leo 2' starring Vijay and Trisha, directed by Lokesh Kanagaraj. Tone: adrenaline-charged, explosive, gritty. Dramatic lighting, volumetric shadows, ultra-detailed textures, high contrast, epic composition, premium typography space, professional film marketing poster, award-winning design style, 8k detail, studio-quality finish."

encoded_prompt = quote_plus(prompt)
api_key = os.getenv('POLLINATIONS_API_KEY', '').strip()

print(f"API Key present: {bool(api_key)}")
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")
print(f"\nPrompt: {prompt[:100]}...")
print(f"\nEncoded prompt (first 100 chars): {encoded_prompt[:100]}...")

# Test 1: With API key (EXACT URL from working script)
if api_key:
    print("\n" + "="*80)
    print("TEST 1: Pollinations with API key (gen.pollinations.ai)")
    print("="*80)
    
    url = f"https://gen.pollinations.ai/image/{encoded_prompt}?model=flux&key={quote_plus(api_key)}"
    print(f"URL: {url[:150]}...")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        print("Sending request...")
        response = requests.get(url, headers=headers, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        print(f"Content Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200 and len(response.content) > 10000:
            output_path = Path("test_poster_with_key.png")
            output_path.write_bytes(response.content)
            print(f"✅ SUCCESS! Poster saved to {output_path}")
        else:
            print(f"❌ FAILED: Status {response.status_code}, Size {len(response.content)}")
            print(f"Response text (first 500 chars): {response.text[:500]}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

# Test 2: Without API key (public endpoint)
print("\n" + "="*80)
print("TEST 2: Pollinations public endpoint (gen.pollinations.ai)")
print("="*80)

url = f"https://gen.pollinations.ai/image/{encoded_prompt}?model=flux"
print(f"URL: {url[:150]}...")

try:
    print("Sending request...")
    response = requests.get(url, timeout=90)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)} bytes")
    print(f"Content Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200 and len(response.content) > 10000:
        output_path = Path("test_poster_public.png")
        output_path.write_bytes(response.content)
        print(f"✅ SUCCESS! Poster saved to {output_path}")
    else:
        print(f"❌ FAILED: Status {response.status_code}, Size {len(response.content)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Simpler prompt
print("\n" + "="*80)
print("TEST 3: Pollinations with simpler prompt")
print("="*80)

simple_prompt = "Cinematic action movie poster for Leo 2 starring Vijay and Trisha"
encoded_simple = quote_plus(simple_prompt)
url = f"https://gen.pollinations.ai/image/{encoded_simple}?model=flux"
print(f"Simple prompt: {simple_prompt}")
print(f"URL: {url}")

try:
    print("Sending request...")
    response = requests.get(url, timeout=90)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)} bytes")
    print(f"Content Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200 and len(response.content) > 10000:
        output_path = Path("test_poster_simple.png")
        output_path.write_bytes(response.content)
        print(f"✅ SUCCESS! Poster saved to {output_path}")
    else:
        print(f"❌ FAILED: Status {response.status_code}, Size {len(response.content)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("TESTS COMPLETE")
print("="*80)
