# parse_chracer.py
# Description: Parses the JSON output from the Chracer tool into a clean CSV format for the dashboard.

import json
import csv
import sys
import os

def parse_chracer_output(input_json_path, output_csv_path):
    """
    Reads a Chracer JSON output file and converts the relevant forensic data into a CSV file.
    """
    print(f"✅ Starting to parse {input_json_path}...")

    try:
        with open(input_json_path, 'r', encoding='utf-8') as infile, \
             open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
            
            # Load the entire JSON data from the Chracer output
            data = json.load(infile)
            
            # Setup the CSV writer and write the header row
            csv_writer = csv.writer(outfile)
            header = ['Timestamp', 'EventType', 'URL', 'WindowTitle', 'IsIncognito']
            csv_writer.writerow(header)

            # --- IMPORTANT ---
            # Loop through the data structure. You may need to adjust these keys 
            # (e.g., 'browser_sessions', 'tabs', 'navigation_history') based on the 
            # actual structure of the chracer_results.json file.
            
            # Assume the top level is a list of browser windows/sessions
            for session in data.get('browser_sessions', []):
                is_incognito = session.get('is_incognito', False)
                
                # Loop through the tabs in each session
                for tab in session.get('tabs', []):
                    
                    # Loop through the browsing history in each tab
                    for event in tab.get('navigation_history', []):
                        timestamp = event.get('timestamp', 'N/A')
                        url = event.get('url', 'N/A')
                        title = event.get('title', 'N/A')
                        
                        # Write the extracted data as a new row in the CSV
                        csv_writer.writerow([timestamp, 'PAGE_VISIT', url, title, is_incognito])
            
            print(f"✅ Successfully parsed the data and saved it to {output_csv_path}")

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{input_json_path}'")
    except json.JSONDecodeError:
        print(f"❌ ERROR: Could not parse the JSON file. It may be corrupted.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 parse_chracer.py <path_to_input.json> <path_to_output.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parse_chracer_output(input_file, output_file)