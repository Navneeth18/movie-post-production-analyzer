# Pollinations AI Integration - Facebook Campaign

## Overview
The Facebook Campaign module now automatically generates AI images for posts using Pollinations AI. No API key required!

## How It Works

### 1. Automatic Image Generation
When you create a Facebook post:
1. Content is generated based on campaign type (teaser, trailer, etc.)
2. An AI prompt is created for the image
3. Pollinations AI generates a movie poster image
4. Image is automatically attached to the Facebook post

### 2. Campaign-Specific Images

Each campaign type gets a unique image style:

**Teaser**
- Mysterious and dramatic
- Dark atmospheric lighting
- Professional movie poster style

**Trailer**
- Epic and action-packed
- Dynamic composition
- Vibrant colors

**Cast Reveal**
- Elegant character showcase
- Professional photography style
- Dramatic lighting

**Countdown**
- Bold typography with clock elements
- Exciting and urgent feel
- Cinematic style

**Release**
- Grand celebration theme
- Spectacular and eye-catching
- Cinema marquee style

### 3. Image Prompts

The system generates detailed prompts like:
```
Cinematic movie teaser poster for 'Baahubali 3', mysterious and dramatic, 
Action, Drama genre, dark atmospheric lighting, professional movie poster 
style, high quality, 4K
```

## Features

### ✅ Automatic Generation
- Images are generated automatically when creating posts
- No manual image upload needed
- Works for all campaign types

### ✅ High Quality
- 1024x1024 resolution
- Enhanced quality mode
- No watermarks

### ✅ Customizable
- Can provide custom image URL instead
- Can disable auto-generation
- Can customize the AI prompt

### ✅ Free Service
- No API key required
- No usage limits
- Instant generation

## Usage

### Backend API

**Generate Content with Image Prompt:**
```python
POST /api/v1/facebook-campaign/{movie_id}/generate-content
{
  "campaign_type": "teaser"
}

Response:
{
  "message": "🎬 Something BIG is coming! 🎬...",
  "hashtags": ["#MovieName", "#Director"],
  "suggestion": "Mysterious teaser image will be auto-generated",
  "image_prompt": "Cinematic movie teaser poster for...",
  "campaign_type": "teaser"
}
```

**Create Post with Auto-Generated Image:**
```python
POST /api/v1/facebook-campaign/{movie_id}/create-post
{
  "message": "Post content",
  "auto_generate_image": true,
  "image_prompt": "Cinematic movie poster..."
}

Response:
{
  "success": true,
  "post_id": "123456789",
  "image_url": "https://image.pollinations.ai/prompt/...",
  "scheduled": false
}
```

### Frontend Usage

1. **Generate Content:**
   - Select campaign type
   - Click "Generate Content"
   - AI prompt is created automatically

2. **Create Post:**
   - Message is pre-filled
   - "Auto-generate AI image" is checked by default
   - Click "Post Now" or "Schedule Post"
   - Image is generated and attached automatically

3. **Custom Image:**
   - Uncheck "Auto-generate AI image"
   - Provide your own image URL
   - Or leave both empty for text-only post

## Technical Details

### Pollinations API
- **Endpoint:** `https://image.pollinations.ai/prompt/{prompt}`
- **Method:** GET (images generated on-demand)
- **Parameters:**
  - `width`: 1024
  - `height`: 1024
  - `nologo`: true
  - `enhance`: true

### Image URL Format
```
https://image.pollinations.ai/prompt/YOUR_PROMPT_HERE?width=1024&height=1024&nologo=true&enhance=true
```

### How Facebook Uses It
1. Post is created with image URL
2. Facebook fetches the image from Pollinations
3. Pollinations generates the image on-demand
4. Image is displayed in the Facebook post

## Testing

### Test Image Generation
```bash
cd backend
python test_pollinations.py
```

This will:
- Generate images for different campaign types
- Show the image URLs
- You can click the URLs to view the generated images

### Example Output
```
✅ Success! Image URL: https://image.pollinations.ai/prompt/...
You can view the image at: [URL]
```

## Configuration

### Environment Variables
No configuration needed! Pollinations is free and doesn't require an API key.

Optional (not used for Pollinations):
```env
POLLINATIONS_API_KEY=sk_VrGtlUl8HjhxeM1jAPTdqm6hLHj9bL23
```

## Advantages

1. **No Setup Required**
   - No API keys
   - No authentication
   - Works immediately

2. **Cost-Effective**
   - Completely free
   - No usage limits
   - No billing

3. **High Quality**
   - Professional-looking posters
   - Consistent style
   - 4K quality

4. **Fast**
   - Images generated on-demand
   - No waiting time
   - Instant URLs

5. **Reliable**
   - Public service
   - High availability
   - No rate limits

## Workflow

### Complete Post Creation Flow

1. **User Action:**
   - Navigate to Facebook Campaign page
   - Select campaign type (e.g., "teaser")
   - Click "Generate Content"

2. **Content Generation:**
   - System generates post message
   - System generates hashtags
   - System creates AI image prompt

3. **Image Generation:**
   - User clicks "Post Now"
   - System generates Pollinations URL
   - Image URL is included in post

4. **Facebook Posting:**
   - Post is sent to Facebook API
   - Facebook fetches image from Pollinations
   - Post appears with AI-generated image

## Customization

### Custom Prompts
You can customize the image prompt in the frontend:
```javascript
const postData = {
  message: "Your message",
  auto_generate_image: true,
  image_prompt: "Your custom prompt here"
}
```

### Disable Auto-Generation
```javascript
const postData = {
  message: "Your message",
  auto_generate_image: false,
  image_url: "https://your-custom-image.jpg"
}
```

## Troubleshooting

### Image Not Showing
- Check if the Pollinations URL is accessible
- Verify Facebook can fetch external images
- Ensure image URL is properly encoded

### Image Quality Issues
- Prompts are optimized for movie posters
- Try adjusting the prompt for better results
- Use more descriptive prompts

### Facebook API Errors
- Ensure Facebook token is valid
- Check if token has `pages_manage_posts` permission
- Verify Page ID is correct

## Future Enhancements

Potential improvements:
- [ ] Image style selection (realistic, artistic, etc.)
- [ ] Multiple image generation (choose best one)
- [ ] Image caching for faster loading
- [ ] Custom image dimensions
- [ ] Batch image generation for campaign schedules

## Examples

### Generated Image URLs

**Teaser for "Baahubali 3":**
```
https://image.pollinations.ai/prompt/Cinematic%20movie%20teaser%20poster%20for%20%27Baahubali%203%27%2C%20mysterious%20and%20dramatic%2C%20Action%2C%20Drama%20genre%2C%20dark%20atmospheric%20lighting%2C%20professional%20movie%20poster%20style%2C%20high%20quality%2C%204K?width=1024&height=1024&nologo=true&enhance=true
```

**Trailer for "RRR 2":**
```
https://image.pollinations.ai/prompt/Epic%20movie%20trailer%20poster%20for%20%27RRR%202%27%2C%20action-packed%20scene%2C%20Action%2C%20Historical%20genre%2C%20dynamic%20composition%2C%20cinematic%20lighting%2C%20professional%20movie%20poster%2C%20vibrant%20colors%2C%204K?width=1024&height=1024&nologo=true&enhance=true
```

## Summary

The Pollinations integration provides:
- ✅ Automatic AI image generation
- ✅ Professional movie poster quality
- ✅ No setup or API keys required
- ✅ Free and unlimited usage
- ✅ Seamless Facebook integration

Your Facebook posts will now automatically include beautiful, AI-generated movie posters!
