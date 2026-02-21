"""
Facebook Automation Service for PR Campaigns
Handles automated posting, scheduling, and analytics for movie promotions
Integrates with Pollinations AI for automatic image generation
"""
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import os
import requests
import urllib.parse
from pathlib import Path
import tempfile

class FacebookService:
    """Service for automating Facebook posts and campaigns"""
    
    def __init__(self):
        self.access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.pollinations_api_key = os.getenv('POLLINATIONS_API_KEY')
        self.api_version = 'v18.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
        # Use the EXACT URL from working script
        self.pollinations_base_url = 'https://gen.pollinations.ai/image'
    
    def build_poster_prompt(self, movie_data: Dict) -> str:
        """
        Build poster prompt exactly like your working code
        
        Args:
            movie_data: Movie information with all required fields
            
        Returns:
            str: Complete poster generation prompt
        """
        movie = movie_data['movie_name']
        hero = movie_data['hero_name']
        heroine = movie_data['heroine_name']
        director = movie_data['director_name']
        genre = movie_data['genre']
        release_date = movie_data.get('release_date')
        requirements_poster = movie_data.get('requirements_poster', '').strip()
        
        # Genre mood mapping (from your code)
        genre_mood_map = {
            "action": "adrenaline-charged, explosive, gritty",
            "romance": "warm, dreamy, emotional",
            "thriller": "tense, mysterious, high-stakes",
            "horror": "ominous, unsettling, atmospheric",
            "drama": "intense, emotional, character-driven",
            "fantasy": "mythic, magical, breathtaking",
            "sci-fi": "futuristic, sleek, awe-inspiring",
            "comedy": "vibrant, energetic, playful",
        }
        
        mood = genre_mood_map.get(genre.strip().lower(), "cinematic, dramatic, immersive")
        
        rd_line = f" Releasing on {release_date}." if release_date else ""
        req_line = f" Additional poster requirements: {requirements_poster}." if requirements_poster else ""
        
        prompt = (
            f"Create a cinematic {genre} movie poster for the film '{movie}' starring "
            f"{hero} and {heroine}, directed by {director}.{rd_line} "
            f"Tone: {mood}. Dramatic lighting, volumetric shadows, ultra-detailed textures, "
            f"high contrast, epic composition, premium typography space, professional film "
            f"marketing poster, award-winning design style, 8k detail, studio-quality finish."
            f"{req_line}"
        )
        
        return prompt
    
    def generate_caption(self, movie_data: Dict) -> str:
        """
        Generate Facebook caption (simplified version of your code)
        
        Args:
            movie_data: Movie information
            
        Returns:
            str: Generated caption with hashtags
        """
        movie = movie_data['movie_name']
        hero = movie_data['hero_name']
        heroine = movie_data['heroine_name']
        director = movie_data['director_name']
        genre = movie_data['genre']
        release_date = movie_data.get('release_date')
        
        release_phrase = f" in theatres on {release_date}" if release_date else " very soon"
        
        caption = (
            f"🎬 Lights, camera, goosebumps! {movie} is bringing pure {genre} energy{release_phrase}. "
            f"Starring {hero} and {heroine}, crafted by {director}. "
            f"Are you ready for the big-screen blast? 🔥 "
            f"Tag your movie squad now! #MovieNight #ComingSoon #CinemaLovers #MustWatch #{movie.replace(' ', '')}"
        )
        
        return caption
    
    def generate_and_save_poster(self, prompt: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Generate poster using AI services and save locally
        Uses EXACT pattern from working script: gen.pollinations.ai/image
        
        Args:
            prompt: Image generation prompt
            output_path: Optional path to save the image
            
        Returns:
            str: Path to saved image file, or None if failed
        """
        try:
            # Encode prompt for URL
            encoded_prompt = urllib.parse.quote_plus(prompt)
            
            # Method 1: Try Pollinations with API key (EXACT URL from working script)
            if self.pollinations_api_key:
                print("Generating poster with Pollinations AI...")
                # EXACT URL format from working script
                url = f"{self.pollinations_base_url}/{encoded_prompt}?model=flux&key={urllib.parse.quote_plus(self.pollinations_api_key)}"
                headers = {"Authorization": f"Bearer {self.pollinations_api_key}"}
                
                try:
                    response = requests.get(url, headers=headers, timeout=60)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        content_length = len(response.content)
                        
                        # Check if it's actually an image
                        if content_length > 10000 and ('image' in content_type or content_length > 50000):
                            if not output_path:
                                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                                output_path = temp_file.name
                                temp_file.close()
                            
                            path = Path(output_path)
                            path.write_bytes(response.content)
                            print(f"✅ Pollinations: AI poster generated successfully ({content_length} bytes)")
                            return str(path)
                        else:
                            print(f"⚠️ Pollinations returned small/invalid content: {content_length} bytes, type: {content_type}")
                    else:
                        error_msg = response.text[:200] if response.text else "No error message"
                        print(f"⚠️ Pollinations API error: Status {response.status_code} - {error_msg}")
                        
                except requests.exceptions.Timeout:
                    print("⚠️ Pollinations request timed out (60s)")
                except Exception as e:
                    print(f"⚠️ Pollinations request failed: {e}")
            else:
                print("⚠️ No Pollinations API key configured (POLLINATIONS_API_KEY)")
            
            # Fallback methods if Pollinations fails
            print("Using fallback poster generation...")
            
            # Method 3: Create a better-looking movie poster using DummyImage
            print("Creating styled movie poster...")
            # Extract movie name from prompt
            movie_name = "Movie Poster"
            if "'" in prompt:
                parts = prompt.split("'")
                if len(parts) >= 2:
                    movie_name = parts[1]
            
            # Create a cinematic-looking poster with gradient
            # Using a service that creates better-looking images
            text = movie_name.replace(' ', '+')
            # Dark cinematic colors
            poster_url = f"https://dummyimage.com/1024x1024/0a0a0a/ff0000.png&text={text}"
            
            try:
                response = requests.get(poster_url, timeout=30)
                if response.status_code == 200:
                    if not output_path:
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        output_path = temp_file.name
                        temp_file.close()
                    
                    path = Path(output_path)
                    path.write_bytes(response.content)
                    print(f"✅ Styled poster created: {path} ({len(response.content)} bytes)")
                    return str(path)
            except Exception as e:
                print(f"Styled poster failed: {e}")
            
            # Method 4: Try placehold.co with better styling
            print("Creating text-based poster with placehold.co...")
            text = movie_name.replace(' ', '+')
            placeholder_url = f"https://placehold.co/1024x1024/1a1a2e/e94560/png?text={text}&font=raleway"
            
            try:
                response = requests.get(placeholder_url, timeout=30)
                if response.status_code == 200:
                    if not output_path:
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        output_path = temp_file.name
                        temp_file.close()
                    
                    path = Path(output_path)
                    path.write_bytes(response.content)
                    print(f"✅ Text poster created: {path} ({len(response.content)} bytes)")
                    return str(path)
            except Exception as e:
                print(f"Text poster failed: {e}")
            
            # Method 5: Last resort - random cinematic image
            print("Using cinematic placeholder...")
            # Use a cinematic/movie-themed placeholder
            placeholder_url = "https://picsum.photos/1024/1024?random=1"
            
            try:
                response = requests.get(placeholder_url, timeout=30)
                if response.status_code == 200:
                    if not output_path:
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                        output_path = temp_file.name
                        temp_file.close()
                    
                    path = Path(output_path)
                    path.write_bytes(response.content)
                    print(f"⚠️ Placeholder image: {path} ({len(response.content)} bytes)")
                    return str(path)
            except Exception as e:
                print(f"Placeholder failed: {e}")
            
            print("❌ All image generation methods failed")
            return None
            
        except Exception as e:
            print(f"Error in generate_and_save_poster: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def generate_campaign_content(movie_data: Dict, campaign_type: str) -> Dict:
        """
        Generate content for different campaign types
        
        Args:
            movie_data: Movie information
            campaign_type: Type of campaign (teaser, trailer, countdown, release)
            
        Returns:
            dict: Generated content with message, hashtags, image prompt, and media suggestions
        """
        
        title = movie_data.get('title', 'Our Movie')
        director = movie_data.get('director', '')
        genres = movie_data.get('genres', [])
        release_date = movie_data.get('release_date')
        
        # Generate hashtags
        hashtags = [
            f"#{title.replace(' ', '')}",
            f"#{director.replace(' ', '')}",
            "#MovieRelease",
            "#ComingSoon"
        ]
        
        # Add genre hashtags
        for genre in genres[:2]:
            hashtags.append(f"#{genre}Movie")
        
        # Generate image prompt for Pollinations
        genre_str = ', '.join(genres[:2]) if genres else 'action'
        
        # Generate content based on campaign type
        if campaign_type == 'teaser':
            message = f"🎬 Something BIG is coming! 🎬\n\n"
            message += f"Get ready for {title}\n"
            message += f"Directed by {director}\n\n"
            message += f"Stay tuned for more updates!\n\n"
            message += " ".join(hashtags)
            
            suggestion = "Mysterious teaser image will be auto-generated"
            image_prompt = f"Cinematic movie teaser poster for '{title}', mysterious and dramatic, {genre_str} genre, dark atmospheric lighting, professional movie poster style, high quality, 4K"
            
        elif campaign_type == 'trailer':
            message = f"🔥 TRAILER ALERT! 🔥\n\n"
            message += f"{title} - Official Trailer\n"
            message += f"Directed by {director}\n\n"
            message += f"Watch now and share your excitement!\n\n"
            message += " ".join(hashtags)
            
            suggestion = "Epic trailer poster will be auto-generated"
            image_prompt = f"Epic movie trailer poster for '{title}', action-packed scene, {genre_str} genre, dynamic composition, cinematic lighting, professional movie poster, vibrant colors, 4K"
            
        elif campaign_type == 'countdown':
            if release_date:
                days_until = (release_date - datetime.now()).days
                message = f"⏰ {days_until} DAYS TO GO! ⏰\n\n"
                message += f"{title} releases on {release_date.strftime('%B %d, %Y')}\n"
                message += f"Directed by {director}\n\n"
                message += f"Mark your calendars! 📅\n\n"
                message += " ".join(hashtags)
            else:
                message = f"Coming Soon! {title}\n\n" + " ".join(hashtags)
            
            suggestion = "Countdown poster will be auto-generated"
            image_prompt = f"Movie countdown poster for '{title}', bold typography with clock elements, {genre_str} genre, exciting and urgent feel, cinematic style, professional design, 4K"
            
        elif campaign_type == 'release':
            message = f"🎉 NOW IN THEATERS! 🎉\n\n"
            message += f"{title} is here!\n"
            message += f"Directed by {director}\n\n"
            message += f"Book your tickets now and experience the magic!\n\n"
            message += " ".join(hashtags)
            
            suggestion = "Release day poster will be auto-generated"
            image_prompt = f"Movie release day poster for '{title}', grand celebration theme, {genre_str} genre, spectacular and eye-catching, cinema marquee style, professional movie poster, vibrant and exciting, 4K"
            
        elif campaign_type == 'cast_reveal':
            cast = movie_data.get('cast', [])
            message = f"⭐ STAR CAST REVEALED! ⭐\n\n"
            message += f"{title}\n"
            if cast:
                message += "Featuring:\n"
                for member in cast[:3]:
                    message += f"• {member.get('name')} as {member.get('role')}\n"
            message += f"\nDirected by {director}\n\n"
            message += " ".join(hashtags)
            
            suggestion = "Cast reveal poster will be auto-generated"
            image_prompt = f"Movie cast reveal poster for '{title}', elegant character showcase, {genre_str} genre, professional photography style, dramatic lighting, movie poster aesthetic, 4K"
            
        else:  # generic
            message = f"🎬 {title} 🎬\n\n"
            message += f"Directed by {director}\n"
            message += f"Coming Soon!\n\n"
            message += " ".join(hashtags)
            
            suggestion = "Movie poster will be auto-generated"
            image_prompt = f"Professional movie poster for '{title}', {genre_str} genre, cinematic style, high quality, 4K"
        
        return {
            'message': message,
            'hashtags': hashtags,
            'suggestion': suggestion,
            'image_prompt': image_prompt,
            'campaign_type': campaign_type
        }
    
    async def create_post(self, movie_data: Dict) -> Dict:
        """
        Create a Facebook post following the exact pattern from your working code
        
        Args:
            movie_data: Complete movie data with all required fields:
                - movie_name, hero_name, heroine_name, director_name, genre
                - release_date (optional), requirements_poster (optional)
            
        Returns:
            dict: Post creation result
        """
        
        # Build prompt and caption (exactly like your code)
        prompt = self.build_poster_prompt(movie_data)
        caption = self.generate_caption(movie_data)
        
        print(f"Generating poster for: {movie_data['movie_name']}")
        print(f"Prompt: {prompt[:100]}...")
        
        # Generate and save poster locally (exactly like your code)
        local_image_path = self.generate_and_save_poster(prompt)
        
        if not local_image_path:
            print("⚠️ Poster generation failed")
            return {
                'success': False,
                'error': 'Failed to generate poster image',
                'mock': False
            }
        
        print(f"✅ Poster generated: {local_image_path}")
        
        if not self.access_token or not self.page_id:
            # Return mock response if credentials not configured
            return self._mock_post_response(caption, None, local_image_path)
        
        try:
            # Upload photo with caption to Facebook (exactly like your code)
            endpoint = f"{self.base_url}/{self.page_id}/photos"
            
            with open(local_image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'access_token': self.access_token,
                    'caption': caption,
                    'published': 'true'
                }
                
                response = requests.post(endpoint, files=files, data=data, timeout=60)
                response.raise_for_status()
            
            # Clean up temp file
            try:
                Path(local_image_path).unlink()
            except:
                pass
            
            result = response.json()
            print(f"✅ Posted to Facebook successfully: {result}")
            
            return {
                'success': True,
                'post_id': result.get('id'),
                'scheduled': False,
                'scheduled_time': None,
                'image_url': local_image_path,
                'caption': caption
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            error_details = {}
            
            try:
                error_data = e.response.json()
                error_details = error_data.get('error', {})
                error_msg = error_details.get('message', str(e))
                error_code = error_details.get('code')
                
                # Provide helpful error messages
                if error_code == 190:
                    error_msg = "Facebook token expired or invalid. Please generate a new token using: python generate_facebook_token.py"
                elif error_code == 200:
                    error_msg = "Missing required Facebook permissions. Token needs 'pages_manage_posts' permission."
                elif error_code == 100:
                    error_msg = "Invalid Facebook Page ID or parameters."
                elif error_code == 324:
                    error_msg = "Image upload failed. The image may be invalid or inaccessible."
            except:
                pass
            
            print(f"Error creating Facebook post: {error_msg}")
            print(f"Full error details: {error_details}")
            
            # Clean up temp file if it exists
            if local_image_path:
                try:
                    Path(local_image_path).unlink()
                except:
                    pass
            
            return {
                'success': False,
                'error': error_msg,
                'error_code': error_details.get('code'),
                'error_type': error_details.get('type'),
                'mock': False
            }
        except Exception as e:
            print(f"Error creating Facebook post: {e}")
            
            # Clean up temp file if it exists
            if local_image_path:
                try:
                    Path(local_image_path).unlink()
                except:
                    pass
            
            return {
                'success': False,
                'error': str(e),
                'mock': False
            }
    
    async def get_post_insights(self, post_id: str) -> Dict:
        """
        Get analytics for a specific post
        
        Args:
            post_id: Facebook post ID
            
        Returns:
            dict: Post insights including reach, engagement, etc.
        """
        
        if not self.access_token:
            return self._mock_insights()
        
        try:
            url = f"{self.base_url}/{post_id}/insights"
            params = {
                'access_token': self.access_token,
                'metric': 'post_impressions,post_engaged_users,post_clicks'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get('data', [])
            
            insights = {}
            for metric in data:
                insights[metric['name']] = metric['values'][0]['value']
            
            return {
                'success': True,
                'impressions': insights.get('post_impressions', 0),
                'engaged_users': insights.get('post_engaged_users', 0),
                'clicks': insights.get('post_clicks', 0)
            }
            
        except Exception as e:
            print(f"Error fetching insights: {e}")
            return self._mock_insights()
    
    async def create_campaign_schedule(
        self,
        movie_data: Dict,
        release_date: datetime,
        campaign_duration_days: int = 30
    ) -> List[Dict]:
        """
        Create a complete campaign schedule leading up to release
        
        Args:
            movie_data: Movie information
            release_date: Movie release date
            campaign_duration_days: How many days before release to start
            
        Returns:
            list: Scheduled posts with dates and content
        """
        
        schedule = []
        start_date = release_date - timedelta(days=campaign_duration_days)
        
        # Campaign milestones
        milestones = [
            {'days_before': 30, 'type': 'teaser', 'title': 'Initial Teaser'},
            {'days_before': 25, 'type': 'cast_reveal', 'title': 'Cast Announcement'},
            {'days_before': 20, 'type': 'trailer', 'title': 'Trailer Release'},
            {'days_before': 15, 'type': 'countdown', 'title': '15 Days Countdown'},
            {'days_before': 10, 'type': 'countdown', 'title': '10 Days Countdown'},
            {'days_before': 7, 'type': 'countdown', 'title': '1 Week Countdown'},
            {'days_before': 3, 'type': 'countdown', 'title': '3 Days Countdown'},
            {'days_before': 1, 'type': 'countdown', 'title': 'Tomorrow!'},
            {'days_before': 0, 'type': 'release', 'title': 'Release Day!'}
        ]
        
        for milestone in milestones:
            days_before = milestone['days_before']
            if days_before <= campaign_duration_days:
                post_date = release_date - timedelta(days=days_before)
                
                # Generate content
                content = self.generate_campaign_content(
                    movie_data,
                    milestone['type']
                )
                
                schedule.append({
                    'title': milestone['title'],
                    'scheduled_date': post_date,
                    'campaign_type': milestone['type'],
                    'message': content['message'],
                    'hashtags': content['hashtags'],
                    'suggestion': content['suggestion'],
                    'status': 'pending'
                })
        
        return schedule
    
    @staticmethod
    def _mock_post_response(message: str, scheduled_time: Optional[datetime], image_url: Optional[str] = None) -> Dict:
        """Return mock response when Facebook API is not configured"""
        return {
            'success': True,
            'post_id': f"mock_{datetime.now().timestamp()}",
            'scheduled': scheduled_time is not None,
            'scheduled_time': scheduled_time.isoformat() if scheduled_time else None,
            'image_url': image_url,
            'mock': True,
            'message': 'Mock post created (Facebook API not configured)'
        }
    
    @staticmethod
    def _mock_insights() -> Dict:
        """Return mock insights when Facebook API is not configured"""
        return {
            'success': True,
            'impressions': 15000,
            'engaged_users': 1200,
            'clicks': 450,
            'mock': True
        }
    
    async def delete_scheduled_post(self, post_id: str) -> Dict:
        """
        Delete a scheduled post
        
        Args:
            post_id: Facebook post ID
            
        Returns:
            dict: Deletion result
        """
        
        if not self.access_token:
            return {'success': True, 'mock': True}
        
        try:
            url = f"{self.base_url}/{post_id}"
            params = {'access_token': self.access_token}
            
            response = requests.delete(url, params=params)
            response.raise_for_status()
            
            return {'success': True}
            
        except Exception as e:
            print(f"Error deleting post: {e}")
            return {'success': False, 'error': str(e)}
