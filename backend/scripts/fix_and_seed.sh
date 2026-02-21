#!/bin/bash

# Fix Duplicate Producers and Seed Movies
# Run this script to fix the duplicate producer issue

echo "================================================================================"
echo "FIX DUPLICATE PRODUCERS & SEED MOVIES"
echo "================================================================================"
echo ""

# Step 1: Verify producers
echo "Step 1: Verifying existing producers in database..."
echo "--------------------------------------------------------------------------------"
python scripts/verify_producers.py

echo ""
echo "================================================================================"
echo "Did you see any MISSING producers above?"
echo "If YES: Register them at http://localhost:5173/register"
echo "        Use credentials from: backend/scripts/producer_credentials.txt"
echo ""
read -p "Press Enter when all producers are registered (or if none are missing)..."
echo ""

# Step 2: Seed movies
echo "Step 2: Seeding movies for existing producers..."
echo "--------------------------------------------------------------------------------"
python scripts/seed_current_movies_existing.py

echo ""
echo "================================================================================"
echo "DONE!"
echo "================================================================================"
echo ""
echo "Next steps:"
echo "1. Login at http://localhost:5173/login"
echo "2. Use any producer credentials from producer_credentials.txt"
echo "3. Go to 'My Movies' to see your projects"
echo "4. All movies release between Feb 23 - March 29, 2026"
echo ""
echo "Example login:"
echo "  Email: dilraju@filmproductions.com"
echo "  Password: Producer@123"
echo ""
echo "================================================================================"
