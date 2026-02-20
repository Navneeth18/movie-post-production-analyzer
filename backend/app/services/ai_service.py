import requests

class AIService:
    def __init__(self, ollama_url):
        self.ollama_url = f"{ollama_url}/api/generate"

    def generate_strategy(self, movie_details):
        prompt = f"As a film marketing expert, suggest a PR strategy for a {movie_details['genre']} movie starring {movie_details['hero']} with an HWS score of {movie_details['score']}."
        
        response = requests.post(self.ollama_url, json={
            "model": "deepseek-r1",
            "prompt": prompt,
            "stream": False
        })
        return response.json().get('response')

    def generate_meme_url(self, genre, theme):
        # Generates a Pollinations.ai URL
        prompt = f"Funny viral movie meme about {genre} and {theme}, cinematic style, high quality"
        formatted_prompt = prompt.replace(" ", "%20")
        return f"https://pollinations.ai/p/{formatted_prompt}?width=1024&height=1024&seed=42"