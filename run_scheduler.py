import time
import subprocess
import sys
from datetime import datetime

def run_update():
    print(f"[{datetime.now()}] Running price update...")
    # Run the management command
    subprocess.run([sys.executable, "manage.py", "update_prices"])
    print(f"[{datetime.now()}] Update complete.")

if __name__ == "__main__":
    print("Starting Price Tracker Scheduler...")
    print("Press Ctrl+C to stop.")
    
    # Run immediately on start
    run_update()
    
    MAX_RETRIES = 3
    RETRY_DELAY = 60  # Seconds

    # Discover every hour
    DISCOVERY_INTERVAL = 3600 
    # Update prices every 4 hours
    UPDATE_INTERVAL = 14400
    
    last_discovery = 0
    last_update = 0

    # Seed URL for discovery (All Cars, sort by Newest)
    SEED_URL = "https://www.donedeal.ie/cars?sort=publishDate%20desc"

    def run_update():
        print(f"[{datetime.now()}] Running price update...")
        try:
             subprocess.run([sys.executable, "manage.py", "update_prices"], check=False)
        except Exception as e:
             print(f"Update failed: {e}")
        print(f"[{datetime.now()}] Update complete.")

    def run_discovery():
        print(f"[{datetime.now()}] Running discovery...")
        try:
             subprocess.run([sys.executable, "manage.py", "discover_ads", SEED_URL], check=False)
        except Exception as e:
             print(f"Discovery failed: {e}")
        print(f"[{datetime.now()}] Discovery complete.")

    try:
        while True:
            now = time.time()
            
            # Check Discovery
            if now - last_discovery > DISCOVERY_INTERVAL:
                run_discovery()
                last_discovery = now
                
            # Check Update
            if now - last_update > UPDATE_INTERVAL:
                run_update()
                last_update = now
                
            time.sleep(60) # Check every minute
            
    except KeyboardInterrupt:
        print("Scheduler stopped.")
