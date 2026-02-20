import sys
import os

# Add the project root to the path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.vector_db import vector_db

def seed_initial_data():
    print("🚀 Initializing Vector DB...")
    vector_db.connect()
    
    # 1. High Hype Reference Data
    hype_samples = [
        "This is going to be a blockbuster! The cinematography is insane.",
        "The background music gave me goosebumps. Pure masterpiece.",
        "Finally, a movie that looks original. Visual effects are Hollywood level.",
        "The lead actor's screen presence is unmatched. Day 1 first show!"
    ]
    
    # 2. Critical/Negative Reference Data
    criticism_samples = [
        "The trailer was disappointing. VFX looks very cheap and outdated.",
        "Bad casting choice. The hero doesn't fit the character at all.",
        "Another routine story. Nothing new to offer for the audience.",
        "The music is too loud and doesn't match the mood of the scenes."
    ]
    
    # Add to collection
    vector_db.add_comments("seed_hype", hype_samples)
    vector_db.add_comments("seed_critics", criticism_samples)
    
    print("✅ Vector DB seeded with 8 reference sentiment points.")

if __name__ == "__main__":
    seed_initial_data()