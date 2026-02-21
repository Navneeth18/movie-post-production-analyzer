# Seed Current Movies Guide - Version 2

## Overview
This script generates realistic current movie projects using existing talent from bob-dataset.csv and bhanu_dataset.csv. All movies are scheduled to release between **February 23 - March 29, 2026** to create a competitive market environment.

## How to Run

```bash
cd backend
python scripts/seed_current_movies_v2.py
```

## Key Features

### Competitive Release Window
- **Start Date**: February 23, 2026
- **End Date**: March 29, 2026
- **Duration**: 34 days
- **Purpose**: Simulates a competitive environment where multiple movies compete for audience attention

### Data Sources
- **Producers**: From bob-dataset.csv (with grades)
- **Directors**: From bob-dataset.csv (with grades)
- **Heroes**: From bhanu_dataset.csv (unique heroes)
- **Heroines**: From bhanu_dataset.csv (unique heroines)

## What It Creates

### 12 Producers (From bob-dataset.csv)
- **2 Grade 1** - High-budget productions (₹15Cr+)
- **4 Grade 2** - Mid-budget productions (₹5-15Cr)
- **6 Grade 3** - Low-budget productions (<₹5Cr)

### 16 Current Movies
All releasing between Feb 23 - March 29, 2026

## Email Format

Emails are generated automatically from producer names:
- **Format**: `firstnamelastname@filmproductions.com`
- **Example**: "Rajesh Kumar" → `rajeshkumar@filmproductions.com`
- **No dots**: Simple format without special characters

## Default Password

All producers use: **`Producer@123`**

## Competitive Environment Benefits

1. **Release Strategy Testing** - See competing movies in same period
2. **Market Analysis** - Multiple movies of different budgets
3. **Realistic Simulation** - Mimics real-world release calendar

## Next Steps

After running:
1. Login with any producer email from `producer_credentials.txt`
2. View your movie's release date
3. Check competitor movies in Release Strategy feature
4. Test Budget Planning for competitive positioning
