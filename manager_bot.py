import subprocess
import time
import json
import os
import sys

# Configurations
MAINTENANCE_FILE = 'maintenance.json'
RUN_TIME_HOURS = 5
MAINTENANCE_TIME_MINS = 10

# Process holders
p_app = None
p_main = None

def set_maintenance(status, duration_secs=0):
    """Update maintenance.json to trigger UI changes in app.py/index.html"""
    end_time = int(time.time() + duration_secs) if status else 0
    data = {"status": status, "end_time": end_time}
    
    with open(MAINTENANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    status_str = "ON" if status else "OFF"
    print(f"[*] Maintenance mode turned {status_str}")

def start_process(script_name):
    """Starts a python script in the background"""
    print(f"[+] Starting {script_name}...")
    # sys.executable ensures it uses the correct Python version (python/python3)
    return subprocess.Popen([sys.executable, script_name])

def stop_process(proc, script_name):
    """Stops a running process"""
    if proc and proc.poll() is None:
        print(f"[-] Stopping {script_name}...")
        proc.terminate()
        proc.wait() # Wait until it fully stops

def main():
    global p_app, p_main
    
    print("=========================================")
    print("    OUT OF LAW - MANAGER BOT STARTED     ")
    print("=========================================\n")
    
    # 1. Ensure maintenance is off on startup
    set_maintenance(False)

    # 2. Start scripts in the requested order
    p_app = start_process('app.py')
    time.sleep(3) # Wait 3 seconds to let the web server start
    
    p_main = start_process('main.py')
    
    print("\n[✓] ALL SYSTEMS ARE ONLINE AND RUNNING!")

    # Convert hours and minutes to seconds
    run_time_secs = RUN_TIME_HOURS * 3600
    maintenance_time_secs = MAINTENANCE_TIME_MINS * 60

    try:
        while True:
            print(f"\n[*] Next maintenance scheduled in {RUN_TIME_HOURS} hours.")
            time.sleep(run_time_secs)

            # ==========================================
            # START MAINTENANCE MODE
            # ==========================================
            print("\n[!] === INITIATING SCHEDULED MAINTENANCE ===")
            
            # Update JSON so website shows maintenance page with 10 mins countdown
            set_maintenance(True, maintenance_time_secs)
            
            # Stop main.py (app.py stays running for the website)
            stop_process(p_main, 'main.py')
            
            print(f"[*] System is resting... Waiting for {MAINTENANCE_TIME_MINS} minutes.")
            time.sleep(maintenance_time_secs)

            # ==========================================
            # END MAINTENANCE MODE
            # ==========================================
            print("\n[!] === ENDING MAINTENANCE ===")
            
            # Turn off maintenance mode in JSON
            set_maintenance(False)
            
            # Restart the scripts
            p_main = start_process('main.py')
            
            print("[✓] SYSTEM RESTORED SUCCESSFULLY!")

    except KeyboardInterrupt:
        # If you press Ctrl+C, it safely closes everything
        print("\n\n[!] Manager Bot stopped manually. Cleaning up processes...")
        stop_process(p_app, 'app.py')
        stop_process(p_main, 'main.py')
        set_maintenance(False)
        print("[✓] All processes closed safely. Exiting.")

if __name__ == "__main__":
    main()