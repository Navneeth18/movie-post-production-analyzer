"""
Data Analytics Service
Provides advanced analytics and visualizations for movie data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

class DataAnalyticsService:
    """Service for data analytics and visualizations"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.bhanu_file = self.data_dir / "bhanu_dataset.csv"
        self.bob_file = self.data_dir / "bob-dataset.csv"
        
    def load_and_clean_data(self):
        """Load and clean both datasets"""
        # Load Bhanu dataset
        bhanu_df = pd.read_csv(self.bhanu_file)
        
        # Convert release_date to datetime
        bhanu_df['release_date'] = pd.to_datetime(bhanu_df['release_date'], format='%d-%m-%Y', errors='coerce')
        
        # Handle missing IMDB ratings with median
        median_rating = bhanu_df['imdb_rating'].median()
        bhanu_df['imdb_rating'].fillna(median_rating, inplace=True)
        
        # Handle missing popularity scores
        median_popularity = bhanu_df['popularity_score'].median()
        bhanu_df['popularity_score'].fillna(median_popularity, inplace=True)
        
        # Load Bob dataset (talent grades)
        bob_df = pd.read_csv(self.bob_file)
        
        return bhanu_df, bob_df
    
    def merge_datasets(self, bhanu_df, bob_df):
        """Merge datasets by matching talent names"""
        # Merge with director grades
        merged_df = bhanu_df.merge(
            bob_df[bob_df['Role'] == 'Director'][['Name', 'Grade']],
            left_on='director',
            right_on='Name',
            how='left',
            suffixes=('', '_director')
        ).rename(columns={'Grade': 'director_grade'})
        
        # Merge with hero grades
        merged_df = merged_df.merge(
            bob_df[bob_df['Role'] == 'Hero'][['Name', 'Grade']],
            left_on='hero',
            right_on='Name',
            how='left',
            suffixes=('', '_hero')
        ).rename(columns={'Grade': 'hero_grade'})
        
        # Merge with heroine grades
        merged_df = merged_df.merge(
            bob_df[bob_df['Role'] == 'Heroine'][['Name', 'Grade']],
            left_on='heroine',
            right_on='Name',
            how='left',
            suffixes=('', '_heroine')
        ).rename(columns={'Grade': 'heroine_grade'})
        
        # Clean up duplicate Name columns
        merged_df = merged_df.drop(columns=[col for col in merged_df.columns if col.startswith('Name')], errors='ignore')
        
        return merged_df
    
    def explode_genres(self, df):
        """Explode multi-label genre column"""
        df_copy = df.copy()
        df_copy['genre'] = df_copy['genre'].str.split(',')
        df_exploded = df_copy.explode('genre')
        df_exploded['genre'] = df_exploded['genre'].str.strip()
        return df_exploded
    
    def explode_age_groups(self, df):
        """Explode multi-label age groups column"""
        df_copy = df.copy()
        df_copy['age_groups_interested'] = df_copy['age_groups_interested'].str.split(',')
        df_exploded = df_copy.explode('age_groups_interested')
        df_exploded['age_groups_interested'] = df_exploded['age_groups_interested'].str.strip()
        return df_exploded
    
    def get_grade_performance_data(self):
        """Get data for grade-performance correlation"""
        bhanu_df, bob_df = self.load_and_clean_data()
        merged_df = self.merge_datasets(bhanu_df, bob_df)
        
        # Filter out rows without director grade
        grade_data = merged_df[merged_df['director_grade'].notna()].copy()
        
        # Group by director grade
        result = []
        for grade in ['Grade 1', 'Grade 2', 'Grade 3']:
            grade_movies = grade_data[grade_data['director_grade'] == grade]
            if len(grade_movies) > 0:
                result.append({
                    'grade': grade,
                    'ratings': grade_movies['imdb_rating'].tolist(),
                    'mean': float(grade_movies['imdb_rating'].mean()),
                    'median': float(grade_movies['imdb_rating'].median()),
                    'count': int(len(grade_movies))
                })
        
        # Find outliers (movies exceeding expectations)
        outliers = []
        for grade in ['Grade 1', 'Grade 2', 'Grade 3']:
            grade_movies = grade_data[grade_data['director_grade'] == grade]
            if len(grade_movies) > 0:
                mean_rating = grade_movies['imdb_rating'].mean()
                std_rating = grade_movies['imdb_rating'].std()
                threshold = mean_rating + (1.5 * std_rating)
                
                top_movies = grade_movies[grade_movies['imdb_rating'] > threshold].nlargest(3, 'imdb_rating')
                for _, movie in top_movies.iterrows():
                    outliers.append({
                        'movie_name': movie['movie_name'],
                        'director': movie['director'],
                        'grade': grade,
                        'rating': float(movie['imdb_rating']),
                        'expected': float(mean_rating),
                        'difference': float(movie['imdb_rating'] - mean_rating)
                    })
        
        return {'data': result, 'outliers': outliers[:10]}
    
    def get_genre_popularity_timeline(self):
        """Get genre popularity over time"""
        bhanu_df, bob_df = self.load_and_clean_data()
        
        # Explode genres
        genre_df = self.explode_genres(bhanu_df)
        
        # Filter valid dates
        genre_df = genre_df[genre_df['release_date'].notna()].copy()
        
        # Extract quarter
        genre_df['quarter'] = genre_df['release_date'].dt.to_period('Q').astype(str)
        
        # Group by quarter and genre
        timeline = genre_df.groupby(['quarter', 'genre'])['popularity_score'].sum().reset_index()
        
        # Pivot for easier frontend consumption
        result = []
        for quarter in timeline['quarter'].unique():
            quarter_data = {'quarter': quarter}
            quarter_df = timeline[timeline['quarter'] == quarter]
            for _, row in quarter_df.iterrows():
                quarter_data[row['genre']] = float(row['popularity_score'])
            result.append(quarter_data)
        
        # Get all unique genres
        genres = sorted(timeline['genre'].unique().tolist())
        
        return {'data': result, 'genres': genres}
    
    def get_talent_value_matrix(self):
        """Get talent value matrix (hero performance)"""
        bhanu_df, bob_df = self.load_and_clean_data()
        merged_df = self.merge_datasets(bhanu_df, bob_df)
        
        # Group by hero
        hero_stats = merged_df.groupby('hero').agg({
            'imdb_rating': 'mean',
            'popularity_score': 'mean',
            'movie_name': 'count'
        }).reset_index()
        
        hero_stats.columns = ['hero', 'avg_imdb', 'avg_popularity', 'movie_count']
        
        # Filter heroes with at least 2 movies
        hero_stats = hero_stats[hero_stats['movie_count'] >= 1]
        
        # Convert to list of dicts
        result = []
        for _, row in hero_stats.iterrows():
            result.append({
                'hero': row['hero'],
                'avg_imdb': float(row['avg_imdb']),
                'avg_popularity': float(row['avg_popularity']),
                'movie_count': int(row['movie_count'])
            })
        
        # Sort by avg_imdb descending
        result = sorted(result, key=lambda x: x['avg_imdb'], reverse=True)
        
        return {'data': result}
    
    def get_demographic_heatmap(self):
        """Get genre-age group correlation heatmap"""
        bhanu_df, bob_df = self.load_and_clean_data()
        
        # Explode both genres and age groups
        genre_df = self.explode_genres(bhanu_df)
        genre_age_df = self.explode_age_groups(genre_df)
        
        # Group by genre and age group
        heatmap_data = genre_age_df.groupby(['genre', 'age_groups_interested'])['popularity_score'].mean().reset_index()
        
        # Pivot to create matrix
        pivot_df = heatmap_data.pivot(index='genre', columns='age_groups_interested', values='popularity_score')
        pivot_df = pivot_df.fillna(0)
        
        # Convert to format suitable for frontend
        genres = pivot_df.index.tolist()
        age_groups = pivot_df.columns.tolist()
        values = pivot_df.values.tolist()
        
        # Convert to list of dicts for easier consumption
        result = []
        for i, genre in enumerate(genres):
            for j, age_group in enumerate(age_groups):
                result.append({
                    'genre': genre,
                    'age_group': age_group,
                    'popularity': float(values[i][j])
                })
        
        return {
            'data': result,
            'genres': genres,
            'age_groups': age_groups
        }
    
    def get_all_analytics(self):
        """Get all analytics data at once"""
        return {
            'grade_performance': self.get_grade_performance_data(),
            'genre_timeline': self.get_genre_popularity_timeline(),
            'talent_matrix': self.get_talent_value_matrix(),
            'demographic_heatmap': self.get_demographic_heatmap()
        }
