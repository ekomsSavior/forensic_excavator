# Forensic Excavator

**Interactive forensic excavation framework for metadata, document artifacts, and redaction failures.**

Forensic Excavator is a Linux-native, analyst-driven triage tool designed to rapidly extract **metadata, hidden text, content streams, strings, and forensic indicators** from documents and datasets at scale.

This tool exists because redactions fail, metadata lies, and documents remember more than their authors intend.

---

## What This Tool Does

Forensic Excavator performs **read-only forensic analysis** across single files or entire datasets, automatically applying the correct tools per file type.

It is built to expose:

* Hidden and residual metadata
* Improper PDF redactions
* Content stream text that visual redactions fail to remove
* Embedded objects and artifacts
* Timeline and provenance indicators
* Raw strings leaked in binary structures
* Chain-of-custody hashes for every file analyzed

This is **triage**, not guessing.
If the data exists, this framework will surface it.

---

## Capabilities

### Universal (All File Types)

* File type identification
* SHA-256 hashing (chain of custody)
* Deep metadata extraction via ExifTool
* Raw string extraction from binaries

### PDF-Specific Forensics

* PDF structure analysis (`pdfinfo`)
* Layout-preserving text extraction (`pdftotext`)
* Content-stream text recovery using PyMuPDF
* Recovery of improperly redacted text objects
* Separation of visible text vs underlying text

### Dataset Support

* Recursive directory analysis
* Automatic handling of mixed file types
* Clean output separation by analysis category

---

## Toolchain Used

This framework deliberately relies on battle-tested open-source forensic tools:

* ExifTool
* poppler-utils (pdfinfo, pdftotext)
* strings (binutils)
* file
* PyMuPDF (fitz)
* Python 3 standard libraries

Nothing proprietary. Nothing cloud-based. Nothing that phones home.

---

## Installation


### 1. System Dependencies

Update your system and install required forensic tools:

```bash
sudo apt update
sudo apt install -y exiftool poppler-utils binutils coreutils python3-pip
```

---

### 2. Python Dependency

Install PyMuPDF for content-stream extraction:

```bash
sudo pip3 install spacy pymupdf --break-system-packages
sudo python3 -m spacy download en_core_web_sm --break-system-packages
```
---

### 3. Clone the Repository

```bash
git clone https://github.com/ekomsSavior/forensic_excavator.git
cd forensic_excavator
```

---

### 4. Permissions

Make the main script executable:

```bash
chmod +x excavator.py
```

---

## Usage

This framework is **fully interactive**.
No arguments. No flags. No shortcuts.

Run it:

```bash
python3 excavator.py
```

You will be prompted:

```
[?] Enter file or directory path to excavate:
```

Examples:

```bash
/home/kali/Documents/redacted.pdf
/home/kali/Datasets/case_files/
/mnt/evidence_drive/
```

The tool will recursively analyze everything under the provided path.

---

## How to Use This to Maximum Effect

### PDF Redaction Failure Analysis

Compare:

* `pdf/file.pdf.text.txt`
* `pdf/unredacted/file.unredacted.txt`

If unredacted output contains data not visible in the document, the redaction failed.

### Metadata Provenance

Inspect:

* `exif/*.exif.txt`

Look for:

* Creator / Producer mismatches
* Editing tools
* Timestamps that don’t align with claims
* Document history artifacts
* XMP remnants

### Binary Leakage

Inspect:

* `strings/*.strings.txt`

Look for:

* Names
* Filenames
* Paths
* URLs
* Internal object references

### Chain of Custody

Use:

* `hashes/*.sha256`

Hashes allow you to:

* Prove files were not altered
* Reproduce findings
* Defend analysis integrity

---

## Disclaimer

This tool is provided **as-is** for lawful forensic analysis, research, investigative journalism, and security testing.

You are solely responsible for:

* How you use it
* What data you analyze
* Whether you have authorization

Use it ethically.
Use it legally.
Misuse is on you, not the author.

