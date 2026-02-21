"""Verify routes are properly configured"""
from app.main import app

print("Verifying Routes Configuration")
print("=" * 70)

routes = []
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        routes.append({
            'path': route.path,
            'methods': list(route.methods) if route.methods else [],
            'name': route.name
        })

# Filter public-pulse routes
public_pulse_routes = [r for r in routes if 'public-pulse' in r['path']]

print(f"\nTotal routes: {len(routes)}")
print(f"Public Pulse routes: {len(public_pulse_routes)}")

if public_pulse_routes:
    print("\nPublic Pulse Routes:")
    print("-" * 70)
    for route in public_pulse_routes:
        methods = ', '.join(route['methods'])
        print(f"  {methods:10} {route['path']}")
    print("\n✓ Public Pulse routes are configured correctly!")
else:
    print("\n✗ No Public Pulse routes found!")
    print("  This means the router is not properly configured.")

# Check movies routes
movies_routes = [r for r in routes if '/movies' in r['path']]
print(f"\nMovies routes: {len(movies_routes)}")
for route in movies_routes[:5]:
    methods = ', '.join(route['methods'])
    print(f"  {methods:10} {route['path']}")

print("\n" + "=" * 70)
print("\nIf Public Pulse routes are shown above, restart the server:")
print("  1. Stop the server (Ctrl+C)")
print("  2. Run: uvicorn app.main:app --reload")
print("  3. The routes will be available at http://localhost:8000")
