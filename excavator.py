#!/usr/bin/env python3

import os
import subprocess
import hashlib
import datetime

# Import PDF unredactor module
from pdf_unredactor import extract_pdf_text

OUTPUT_DIR = "output"

def banner():
    print("""
===========================================
   FORENSIC EXCAVATOR v1.1
   Interactive Metadata & Data Miner
   + PDF Content Stream Unredaction
===========================================
    """)

def run(cmd, outfile=None):
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        if outfile:
            with open(outfile, "wb") as f:
                f.write(result)
        return result.decode(errors="ignore")
    except subprocess.CalledProcessError as e:
        return e.output.decode(errors="ignore")

def hash_file(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha.update(block)
    return sha.hexdigest()

def ensure_dirs():
    dirs = [
        "exif",
        "pdf",
        "pdf/unredacted",
        "strings",
        "hashes",
        "logs"
    ]
    for d in dirs:
        os.makedirs(os.path.join(OUTPUT_DIR, d), exist_ok=True)

def analyze_file(path):
    name = os.path.basename(path)

    print(f"\n[+] Analyzing: {path}")

    # Identify file type
    filetype = run(["file", path])
    print(f"    Type: {filetype.strip()}")

    # Hash (chain of custody)
    sha = hash_file(path)
    with open(f"{OUTPUT_DIR}/hashes/{name}.sha256", "w") as f:
        f.write(sha)

    # Deep metadata extraction
    run(
        ["exiftool", "-a", "-u", "-g1", "-ee", path],
        f"{OUTPUT_DIR}/exif/{name}.exif.txt"
    )

    # Raw strings extraction
    run(
        ["strings", "-n", "6", path],
        f"{OUTPUT_DIR}/strings/{name}.strings.txt"
    )

    # -------------------------
    # PDF-SPECIFIC FORENSICS
    # -------------------------
    if "PDF" in filetype:
        print("    [*] PDF detected — running PDF forensics")

        run(
            ["pdfinfo", path],
            f"{OUTPUT_DIR}/pdf/{name}.pdfinfo.txt"
        )

        run(
            ["pdftotext", "-layout", path, f"{OUTPUT_DIR}/pdf/{name}.text.txt"]
        )

        # PyMuPDF content-stream extraction (unredaction)
        try:
            out_file, size = extract_pdf_text(
                path,
                f"{OUTPUT_DIR}/pdf/unredacted"
            )
            print(f"    [!] Unredacted text extracted ({size} chars)")
        except Exception as e:
            print(f"    [-] Unredaction failed: {e}")

def walk_dataset(target):
    if os.path.isfile(target):
        analyze_file(target)
    else:
        for root, _, files in os.walk(target):
            for f in files:
                full = os.path.join(root, f)
                analyze_file(full)

def main():
    banner()
    ensure_dirs()

    target = input("[?] Enter file or directory path to excavate: ").strip()

    if not os.path.exists(target):
        print("[-] Path does not exist.")
        return

    log = f"{OUTPUT_DIR}/logs/session_{datetime.datetime.now().isoformat()}.log"
    with open(log, "w") as f:
        f.write(f"Target: {target}\n")

    walk_dataset(target)

    print("\n[✓] Excavation complete.")
    print(f"[✓] Results saved in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
