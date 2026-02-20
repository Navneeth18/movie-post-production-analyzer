# HWS Score Weights
Wd = 0.25  # Director weight
Wh = 0.20  # Historical performance weight
Ws = 0.15  # Sentiment weight
Wp = 0.15  # Pulse weight
Wg = 0.10  # Genre weight
Wb = 0.10  # Budget weight
Wt = 0.05  # Timing weight

# Grade mapping for artists
GRADE_MAP = {
    "Grade 1": 100,
    "Grade 2": 40,
    "Grade 3": 10
}

# Component weights for HWS calculation
WEIGHTS = {
    "director": 0.25,
    "hero": 0.15,
    "genre": 0.20,
    "popularity": 0.15,
    "heroine": 0.08,
    "producer": 0.07,
    "imdb": 0.10
}