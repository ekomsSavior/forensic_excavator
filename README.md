# Forensic Excavator

**Interactive forensic excavation framework for metadata, document artifacts, redaction failures, and provenance analysis.**

Forensic Excavator is a Linux-native, analyst-driven forensic triage framework designed to excavate **metadata, hidden text, content streams, embedded artifacts, entities, and timelines** from documents and datasets at scale.

---

## What Forensic Excavator Does

Forensic Excavator performs **read-only forensic analysis** against individual files or entire datasets.
It automatically applies the appropriate forensic tooling based on file type and surfaces findings **both in the terminal and as preserved artifacts on disk**.

It is built to expose:

* Hidden and residual metadata
* Improper and incomplete PDF redactions
* Content-stream text surviving visual redaction
* Embedded objects and binary artifacts
* Named entities (people, organizations, locations, dates)
* Timeline and provenance indicators
* Raw strings leaked in binary structures
* Sanitization and structural failures in PDFs
* Cryptographic hashes for chain of custody

This is forensic triage, not guesswork.
If the data exists, this framework is designed to surface it.

---

## Capabilities

### Universal (All File Types)

* File type identification
* SHA-256 hashing for chain of custody
* Deep metadata extraction via ExifTool
* Raw string extraction from binary data
* Filesystem timestamp capture for timeline reconstruction
* Terminal output of key forensic findings

---

### PDF-Specific Forensics

* Structural analysis (`pdfinfo`)
* Layout-preserving text extraction (`pdftotext`)
* Content-stream text recovery using PyMuPDF
* Detection of improperly redacted text objects
* Automatic bad-redaction flagging
* PDF sanitization and structural validation via `qpdf`
* Separation of visible text vs underlying content
* Entity extraction from recovered and visible text

---

### Image & Binary Analysis

* Embedded payload and artifact discovery using `binwalk`
* Identification of hidden or appended data in image files

---

### Entity Extraction

* Automated extraction of:

  * Persons
  * Organizations
  * Locations
  * Dates
* Uses spaCy with a locally installed language model

---

### Timeline Reconstruction

* Filesystem creation and modification timestamps
* Metadata-derived document timestamps
* Per-file timeline artifacts suitable for correlation and reporting

---

### Dataset Support

* Recursive directory analysis
* Mixed file-type handling
* Clean separation of forensic artifacts by category
* Scales from single documents to mounted evidence volumes
---

## Installation

### 1. System Dependencies

```bash
sudo apt update
sudo apt install -y exiftool poppler-utils binutils coreutils binwalk qpdf python3-pip
```
---

### 2. Python Dependencies (Required)

Forensic Excavator **requires spaCy and its language model**.

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

```bash
chmod +x excavator.py
```

---

## Usage

Forensic Excavator is fully interactive.

No arguments.
No flags.
No shortcuts.

Run:

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

All files under the specified path will be analyzed recursively.

---


## How to Use This to Maximum Effect

### PDF Redaction Failure Detection

Compare:

* `output/pdf/<file>.text.txt`
* `output/pdf/unredacted/<file>.unredacted.txt`

If recovered text contains information not visible in the rendered document, the redaction failed.

The framework will automatically flag suspected redaction failures during analysis.

---

### Entity Intelligence

Review:

```bash
output/entities/<file>.entities.txt
```

Use this to:

* Identify individuals, organizations, and locations
* Correlate entities across multiple documents
* Build investigative leads rapidly

---

### Metadata & Provenance Analysis

Inspect:

```bash
output/exif/*.exif.txt
```

Focus on:

* Creator and Producer inconsistencies
* Editing tools and workflows
* Timestamp conflicts
* XMP and document history remnants

---

### Embedded & Binary Artifact Discovery

Review:

```bash
output/strings/
output/binwalk/
```

Look for:

* Embedded file signatures
* Residual filenames and paths
* URLs, identifiers, and object references

---

### Chain of Custody

Use:

```bash
output/hashes/*.sha256
```

Hashes allow you to:

* Verify integrity
* Reproduce findings
* Defend analysis in adversarial settings

---

## Disclaimer

This tool is provided **as-is** for lawful forensic analysis, investigative research, journalism, and security testing.

You are solely responsible for:

* Authorization to analyze the data
* Legal and ethical use
* Interpretation of findings

The author assumes no liability for misuse.

