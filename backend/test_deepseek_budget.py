"""
Test DeepSeek R1 integration for budget optimization
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

def test_deepseek_budget_optimization():
    """Test DeepSeek R1 for budget optimization"""
    
    print("="*80)
    print("Testing DeepSeek R1 Budget Optimization")
    print("="*80)
    
    # Sample budget data
    prompt = """You are a film marketing budget optimization expert specializing in Indian cinema. Analyze this budget allocation and provide tactical recommendations.

Film Details:
- Title: "Leo 2"
- Genre: Action
- Production Budget: ₹50.00Cr
- Marketing Budget: ₹5.00Cr
- Campaign Timeline: 8 weeks before release

Current Channel Allocation:
- Digital Marketing: 30% (₹1.50Cr) - ROI: 3.2x
- Traditional Media: 15% (₹0.75Cr) - ROI: 1.8x
- Influencer Marketing: 20% (₹1.00Cr) - ROI: 2.5x
- Events & Activations: 10% (₹0.50Cr) - ROI: 2.0x
- PR & Media Relations: 15% (₹0.75Cr) - ROI: 2.8x
- Contingency Reserve: 10% (₹0.50Cr)

Provide brief recommendations in these sections:
1. BUDGET OPTIMIZATION - Which channels to adjust
2. CHANNEL TACTICS - Key strategies for Action genre
3. TIMELINE STRATEGY - 8-week breakdown
4. RISK MITIGATION - Key risks to watch
5. ROI IMPROVEMENTS - Expected improvements

Keep response concise and actionable."""

    print(f"\nOllama URL: {OLLAMA_URL}")
    print(f"Model: deepseek-r1:7b")
    print(f"\nPrompt length: {len(prompt)} characters")
    print("\nSending request to DeepSeek R1...")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "deepseek-r1:7b",  # Use the full model name
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('response', '')
            
            print(f"\n✅ SUCCESS!")
            print(f"Response length: {len(recommendations)} characters")
            print(f"\n{'='*80}")
            print("RECOMMENDATIONS:")
            print("="*80)
            print(recommendations[:1000])  # First 1000 chars
            if len(recommendations) > 1000:
                print(f"\n... (truncated, total {len(recommendations)} characters)")
            print("="*80)
            
            return True
        else:
            print(f"\n❌ FAILED")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ TIMEOUT - Request took longer than 120 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR - Cannot connect to Ollama at {OLLAMA_URL}")
        print("Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ollama_status():
    """Check if Ollama is running and has deepseek-r1"""
    print("\n" + "="*80)
    print("Checking Ollama Status")
    print("="*80)
    
    try:
        # Check if Ollama is running
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            print(f"✓ Ollama is running at {OLLAMA_URL}")
            print(f"✓ Available models: {len(models)}")
            
            # Check for deepseek-r1
            deepseek_models = [m for m in model_names if 'deepseek' in m.lower()]
            
            if deepseek_models:
                print(f"✓ DeepSeek models found: {deepseek_models}")
                return True
            else:
                print(f"⚠ DeepSeek R1 not found in available models")
                print(f"  Available: {model_names}")
                print(f"\nTo install DeepSeek R1, run:")
                print(f"  ollama pull deepseek-r1")
                return False
        else:
            print(f"✗ Ollama returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama at {OLLAMA_URL}")
        print(f"  Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False

if __name__ == "__main__":
    # First check Ollama status
    ollama_ok = test_ollama_status()
    
    if ollama_ok:
        # Then test budget optimization
        success = test_deepseek_budget_optimization()
        
        if success:
            print("\n" + "="*80)
            print("✅ ALL TESTS PASSED - DeepSeek R1 is working!")
            print("="*80)
        else:
            print("\n" + "="*80)
            print("❌ TESTS FAILED - Check errors above")
            print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ Ollama not ready - Fix Ollama setup first")
        print("="*80)
