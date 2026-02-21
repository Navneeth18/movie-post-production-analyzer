# Score System Explanation

## Overview
The system uses two main scores to evaluate movies: **Cast Score** and **HWS Score**.

## 1. Cast Score

### What It Is
A measure of the star power of the actors in the movie.

### How It's Calculated
- Looks up Hero and Heroine in the artists database
- Each artist has a grade: Grade 1, Grade 2, or Grade 3
- Uses exponential scoring:
  - **Grade 1** (Elite): 100 points
  - **Grade 2** (Established): 40 points
  - **Grade 3** (Newcomer): 10 points
- Weighted average: **60% Hero + 40% Heroine**

### Example
```
Hero: Prabhas (Grade 1) = 100
Heroine: Anushka Shetty (Grade 3) = 10

Cast Score = (100 × 0.6) + (10 × 0.4)
           = 60 + 4
           = 64
```

### What It Tells You
- How strong the lead actors are
- The drawing power of the cast
- Initial audience attraction based on stars

---

## 2. HWS Score (Historical Weighted Score)

### What It Is
A comprehensive prediction of movie success using 7 factors with market-adjusted weights.

### The Formula
```
HWS = (Director × 25%) + (Genre × 20%) + (Hero × 15%) + 
      (Popularity × 15%) + (Predicted IMDb × 10%) + 
      (Heroine × 8%) + (Producer × 7%)
```

### The 7 Factors

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Director** | 25% | Director's brand and track record (Grade 1/2/3) |
| **Genre** | 20% | How trending the genre is (Action=90, Thriller=85, etc.) |
| **Hero** | 15% | Lead actor's star power (Grade 1/2/3) |
| **Popularity** | 15% | Public Pulse from YouTube sentiment analysis |
| **Predicted IMDb** | 10% | Estimated rating based on director + genre history |
| **Heroine** | 8% | Lead actress's star power (Grade 1/2/3) |
| **Producer** | 7% | Producer's resources and distribution capability |

### Categories

Based on the HWS score, movies are categorized:

| HWS Range | Category | Market Action |
|-----------|----------|---------------|
| 75-100 | **BIG** | Global theatrical release; Massive marketing spend |
| 45-74 | **MEDIUM** | Targeted regional release; High PR influencer focus |
| 0-44 | **SMALL** | OTT-First strategy or hyper-niche community marketing |

### Example Calculation

**Movie: Baahubali-style Epic**
- Director: S. S. Rajamouli (Grade 1) = 100 → 100 × 0.25 = **25.0**
- Genre: Action = 90 → 90 × 0.20 = **18.0**
- Hero: Prabhas (Grade 1) = 100 → 100 × 0.15 = **15.0**
- Popularity: High buzz = 85 → 85 × 0.15 = **12.75**
- Predicted IMDb: 97 → 97 × 0.10 = **9.7**
- Heroine: Anushka (Grade 3) = 10 → 10 × 0.08 = **0.8**
- Producer: Unknown (Grade 3) = 10 → 10 × 0.07 = **0.7**

**Total HWS = 81.95** → **Category: BIG**

### What It Tells You
- Overall success prediction
- Market positioning (BIG/MEDIUM/SMALL)
- Recommended marketing strategy
- Competitive strength

---

## Key Differences

| Aspect | Cast Score | HWS Score |
|--------|-----------|-----------|
| **Focus** | Only actors | 7 comprehensive factors |
| **Range** | 10-100 | 0-100 |
| **Purpose** | Star power | Success prediction |
| **Factors** | 2 (Hero + Heroine) | 7 (Director, Genre, Cast, etc.) |
| **Weight** | Equal importance | Market-adjusted weights |
| **Output** | Single number | Number + Category + Strategy |

---

## Why Both Scores?

### Cast Score
- Quick indicator of star power
- Easy to understand
- Useful for initial assessment
- Important for opening weekend

### HWS Score
- Comprehensive success prediction
- Considers market trends
- Includes director's impact
- Factors in public sentiment
- Provides strategic guidance

---

## In the UI

### Movie Cards
```
┌─────────────────────┐
│ Movie Title         │
│ Cast: 64  HWS: 82   │
│         [BIG]       │
└─────────────────────┘
```

### Movie Detail Page
```
┌──────────────┐ ┌──────────────┐
│ Cast Score   │ │ HWS Score    │
│    64.0      │ │   81.9 [BIG] │
│ Star power   │ │ Global...    │
└──────────────┘ └──────────────┘
```

### Dashboard
```
Avg Cast Score: 64.5
```

---

## For Producers

### Use Cast Score When:
- Evaluating star power
- Planning initial marketing
- Negotiating with actors
- Estimating opening weekend

### Use HWS Score When:
- Making release decisions
- Planning overall strategy
- Comparing with competitors
- Deciding marketing budget
- Choosing release windows

---

## Summary

- **Cast Score** = Actor star power (simple, focused)
- **HWS Score** = Comprehensive success prediction (complex, strategic)
- Both are important for different purposes
- HWS includes cast as one of 7 factors
- HWS provides category and strategy recommendations
