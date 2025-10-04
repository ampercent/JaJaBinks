# analyze_layer1.py
# Author: [haiyuujikun]
# Date: 04-Oct-2025
# Description: Automates Layer 1 forensic analysis by running Volatility 3 (with PyPy)
#              and Bulk Extractor on a given memory dump.

import subprocess
import os
import sys
from datetime import datetime

def run_analysis(memory_dump_path):
    """
    Main function to run the Layer 1 forensic toolchain.
    """
    # --- 1. Validate Input File ---
    if not os.path.exists(memory_dump_path):
        print(f"❌ ERROR: Memory dump file not found at '{memory_dump_path}'")
        sys.exit(1)

    print("✅ Starting Layer 1 Forensic Analysis...")
    print(f"   Target file: {memory_dump_path}")

    # --- 2. Create a Timestamped Results Directory ---
    # Assuming the project is on the Desktop as discussed
    base_dir = os.path.expanduser("~/Desktop/Forensics_Project/Evidence")
    results_dir = os.path.join(base_dir, f"Layer1_Results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    try:
        os.makedirs(results_dir)
        print(f"✅ Results will be saved in: {results_dir}")
    except OSError as e:
        print(f"❌ ERROR: Could not create results directory. {e}")
        sys.exit(1)

    # --- 3. Define Tool Paths ---
    # Assumes tools are in the specified project structure on your Linux Mint machine
    volatility_path = os.path.expanduser("~/Desktop/Forensics_Project/Tools/volatility3/vol.py")

    # --- 4. Run Volatility 'pslist' ---
    print("\n[+] Running Volatility 'pslist'...")
    pslist_output_path = os.path.join(results_dir, "pslist.txt")
    vol_command_pslist = [
        "pypy3", 
        volatility_path,
        "-f", memory_dump_path,
        "windows.pslist"
    ]
    try:
        with open(pslist_output_path, "w") as outfile:
            subprocess.run(vol_command_pslist, stdout=outfile, stderr=subprocess.STDOUT, text=True, check=True)
        print("    -> 'pslist' complete. Output saved to pslist.txt")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"    -> ❌ FAILED to run 'pslist'. Error: {e}")
        print("    -> Make sure 'pypy3' is in your PATH and Volatility is at the correct location.")

    # --- 5. Run Volatility 'netscan' ---
    print("\n[+] Running Volatility 'netscan'...")
    netscan_output_path = os.path.join(results_dir, "netscan.txt")
    vol_command_netscan = [
        "pypy3",
        volatility_path,
        "-f", memory_dump_path,
        "windows.netscan"
    ]
    try:
        with open(netscan_output_path, "w") as outfile:
            subprocess.run(vol_command_netscan, stdout=outfile, stderr=subprocess.STDOUT, text=True, check=True)
        print("    -> 'netscan' complete. Output saved to netscan.txt")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"    -> ❌ FAILED to run 'netscan'. Error: {e}")

    # --- 6. Run Bulk Extractor ---
    print("\n[+] Running Bulk Extractor (this may take a while)...")
    bulk_output_dir = os.path.join(results_dir, "bulk_extractor_output")
    bulk_command = [
        "bulk_extractor",
        "-o", bulk_output_dir,
        memory_dump_path
    ]
    try:
        subprocess.run(bulk_command, capture_output=True, text=True, check=True)
        print(f"    -> Bulk Extractor complete. Output saved to '{bulk_output_dir}'")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"    -> ❌ FAILED to run Bulk Extractor. Error: {e}")
        print("    -> Make sure 'bulk_extractor' is installed and in your system's PATH.")

    print("\n✅ Layer 1 analysis finished!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_layer1.py <path_to_memory_dump>")
        sys.exit(1)
    
    target_file = sys.argv[1]
    run_analysis(target_file)