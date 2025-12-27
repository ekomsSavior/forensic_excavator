#!/usr/bin/env python3

import os
import subprocess
import hashlib
import datetime
import re
import spacy

from pdf_unredactor import extract_pdf_text

nlp = spacy.load("en_core_web_sm")

OUTPUT_DIR = "output"

def banner():
    print("""
===========================================
   FORENSIC EXCAVATOR v2.0
   Interactive Forensic Excavation Console
===========================================
    """)

def run(cmd, outfile=None, show=False, max_lines=25):
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        text = result.decode(errors="ignore")
        if outfile:
            with open(outfile, "wb") as f:
                f.write(result)
        if show:
            print("\n".join(text.splitlines()[:max_lines]))
        return text
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
        "exif", "pdf", "pdf/unredacted", "strings",
        "hashes", "logs", "entities", "timeline",
        "binwalk", "qpdf"
    ]
    for d in dirs:
        os.makedirs(os.path.join(OUTPUT_DIR, d), exist_ok=True)

def extract_entities(text, outfile):
    doc = nlp(text)
    ents = sorted(set(f"{ent.text} [{ent.label_}]" for ent in doc.ents))
    with open(outfile, "w") as f:
        for e in ents:
            f.write(e + "\n")
    return ents

def timeline_event(label, value, outfile):
    with open(outfile, "a") as f:
        f.write(f"{label}: {value}\n")

def analyze_file(path):
    name = os.path.basename(path)
    print(f"\n[+] Analyzing: {path}")

    filetype = run(["file", path])
    print(f"    Type: {filetype.strip()}")

    sha = hash_file(path)
    with open(f"{OUTPUT_DIR}/hashes/{name}.sha256", "w") as f:
        f.write(sha)

    timeline = f"{OUTPUT_DIR}/timeline/{name}.timeline.txt"
    stat = os.stat(path)
    timeline_event("Filesystem Created", datetime.datetime.fromtimestamp(stat.st_ctime), timeline)
    timeline_event("Filesystem Modified", datetime.datetime.fromtimestamp(stat.st_mtime), timeline)

    exif = run(
        ["exiftool", "-a", "-u", "-g1", "-ee", path],
        f"{OUTPUT_DIR}/exif/{name}.exif.txt"
    )

    run(["strings", "-n", "6", path], f"{OUTPUT_DIR}/strings/{name}.strings.txt")

    if "PDF" in filetype:
        print("    [*] PDF detected")

        pdfinfo = run(
            ["pdfinfo", path],
            f"{OUTPUT_DIR}/pdf/{name}.pdfinfo.txt"
        )

        pdftxt = run(
            ["pdftotext", "-layout", path, f"{OUTPUT_DIR}/pdf/{name}.text.txt"]
        )

        # --- UNREDACTION ---
        try:
            unredacted_file, size = extract_pdf_text(path, f"{OUTPUT_DIR}/pdf/unredacted")
            print(f"    [!] Unredacted text recovered: {size} chars")

            visible_len = len(pdftxt)
            if size > visible_len * 1.2:
                print("    [!!!] BAD REDACTION FLAG TRIGGERED")

            with open(unredacted_file, "r", errors="ignore") as f:
                text = f.read()

            ents = extract_entities(
                text,
                f"{OUTPUT_DIR}/entities/{name}.entities.txt"
            )

            print(f"    [+] Entities extracted: {len(ents)}")

        except Exception as e:
            print(f"    [-] Unredaction failed: {e}")

        # --- QPDF CHECK ---
        run(
            ["qpdf", "--check", path],
            f"{OUTPUT_DIR}/qpdf/{name}.qpdf.txt",
            show=True
        )

    # --- BINWALK FOR IMAGES ---
    if any(x in filetype.lower() for x in ["image", "jpeg", "png"]):
        print("    [*] Image detected — running binwalk")
        run(
            ["binwalk", path],
            f"{OUTPUT_DIR}/binwalk/{name}.binwalk.txt",
            show=True
        )

def walk_dataset(target):
    if os.path.isfile(target):
        analyze_file(target)
    else:
        for root, _, files in os.walk(target):
            for f in files:
                analyze_file(os.path.join(root, f))

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

    print("\n[✓] Excavation complete")
    print("[✓] Artifacts saved to ./output/")

if __name__ == "__main__":
    main()
