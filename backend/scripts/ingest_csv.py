import pandas as pd
from pymongo import MongoClient
import os

def ingest_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["film_intel_db"]
    
    # Ingest BOB Dataset (Artists)
    if os.path.exists("data/bob-dataset.csv"):
        bob_df = pd.read_csv("data/bob-dataset.csv")
        db.artists.drop() # Refresh collection
        db.artists.insert_many(bob_df.to_dict("records"))
        print(f"Ingested {len(bob_df)} artists into MongoDB.")

    # Ingest Bhanu Dataset (Historical Movies)
    if os.path.exists("data/bhanu_dataset.csv"):
        bhanu_df = pd.read_csv("data/bhanu_dataset.csv")
        db.historical_movies.drop()
        db.historical_movies.insert_many(bhanu_df.to_dict("records"))
        print(f"Ingested {len(bhanu_df)} historical movies into MongoDB.")

if __name__ == "__main__":
    ingest_data()