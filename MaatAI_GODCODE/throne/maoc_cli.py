#!/usr/bin/env python3
"""
MAOC CLI - Command Line Interface
Run from terminal: python3 maoc_cli.py
"""

import sys
import os

# Add throne directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maoc import MAOC

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ███╗ ██████╗ ██╗     ██████╗ ███████╗ ██████╗     ║
║   ████╗ ████║██╔═══██╗██║     ██╔══██╗██╔════╝██╔═══██╗    ║
║   ██╔████╔██║██║   ██║██║     ██║  ██║█████╗  ██║   ██║    ║
║   ██║╚██╔╝██║██║   ██║██║     ██║  ██║██╔══╝  ██║   ██║    ║
║   ██║ ╚═╝ ██║╚██████╔╝███████╗██████╔╝██║     ╚██████╔╝    ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝      ╚═════╝     ║
║                                                              ║
║     MARITIME & AVIATION OPERATIONS CENTER                   ║
║              Throne Integrated v1.0                         ║
╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    print_banner()
    
    maoc = MAOC()
    
    if not maoc.initialize():
        print("\n❌ Failed to initialize MAOC")
        sys.exit(1)
    
    print("\n📡 Fetching initial data...")
    maoc.update_all()
    
    import json
    
    # Show overview
    overview = maoc.get_overview()
    print("\n📊 OVERVIEW:")
    print(f"   ✈️  Aircraft: {overview['air_traffic'].get('aircraft_count', 0)}")
    print(f"   🚢 Vessels:  {overview['maritime'].get('vessel_count', 0)}")
    print(f"   📍 Total:    {overview['total_tracked']}")
    
    # Interactive loop
    print("\n" + "=" * 50)
    print("COMMANDS:")
    print("  search <query>     - Search aircraft/vessels")
    print("  nearby <lat> <lon> [km] - Find nearby traffic")
    print("  refresh            - Update all data")
    print("  overview           - Show statistics")
    print("  events             - Major events")
    print("  export             - Export all data to JSON")
    print("  quit               - Exit")
    print("=" * 50 + "\n")
    
    while True:
        try:
            cmd = input("MAOC> ").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0].lower()
            
            if command == "quit" or command == "exit":
                print("\n👋 Shutting down MAOC...")
                break
            
            elif command == "help":
                print("""
  search <query>     - Search aircraft/vessels
  nearby <lat> <lon> [km] - Find nearby traffic
  refresh            - Update all data
  overview           - Show statistics
  events             - Major events
  export             - Export all data to JSON
  quit               - Exit
                """)
            
            elif command == "refresh" or command == "update":
                print("📡 Updating data...")
                maoc.update_all()
                print("✅ Updated")
            
            elif command == "overview" or command == "stats":
                overview = maoc.get_overview()
                print(json.dumps(overview, indent=2))
            
            elif command == "search":
                if len(parts) < 2:
                    print("Usage: search <query>")
                    continue
                query = " ".join(parts[1:])
                results = maoc.search_all(query)
                print(f"Found {len(results['aircraft'])} aircraft, {len(results['vessels'])} vessels")
                print(json.dumps(results, indent=2))
            
            elif command == "nearby":
                if len(parts) < 3:
                    print("Usage: nearby <lat> <lon> [radius_km]")
                    continue
                lat = float(parts[1])
                lon = float(parts[2])
                radius = float(parts[3]) if len(parts) > 3 else 100
                nearby = maoc.get_nearby(lat, lon, radius)
                print(f"Near ({lat}, {lon}): {len(nearby['aircraft'])} aircraft, {len(nearby['vessels'])} vessels")
                print(json.dumps(nearby, indent=2))
            
            elif command == "events":
                events = maoc.get_major_events()
                print(json.dumps(events, indent=2))
            
            elif command == "export":
                data = maoc.export_full_data()
                filename = f"/tmp/maoc_export_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    f.write(data)
                print(f"✅ Exported to {filename}")
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down MAOC...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import time
    main()
