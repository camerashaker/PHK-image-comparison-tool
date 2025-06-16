# USPS Tracking Tool (Python Version)

A high-performance Python implementation that scrapes USPS tracking information for multiple tracking numbers concurrently.

## Features

- **Concurrent Processing**: Process multiple tracking numbers simultaneously using multiple headless Chrome browsers
- **Reliable Parsing**: Extracts detailed tracking history, status updates, and delivery information
- **Performance Optimized**: Much faster than PowerShell implementation by using headless Chrome and multithreading
- **No API Keys Required**: Works directly with the public USPS tracking website
- **Cross-Platform**: Works on macOS, Windows, and Linux

## Requirements

- Python 3.7+
- Chrome browser installed
- Python dependencies (install via pip):
  ```
  pip install -r requirements.txt
  ```

## Installation

1. Clone or download this repository
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Ensure Chrome browser is installed on your system

## Usage

### Basic Usage

```bash
python usps_tracking.py -i input.csv -c "Tracking Number"
```

Where:
- `input.csv` is your CSV file containing tracking numbers
- `"Tracking Number"` is the column name in the CSV containing the tracking numbers

### Advanced Options

```bash
python usps_tracking.py -i input.csv -o results.csv -c "Tracking Number" -w 8 -d 1 -m 100 --debug-dir debug
```

Parameters:
- `-i, --input`: Input CSV file path (REQUIRED)
- `-o, --output`: Output CSV file path (default: input_results.csv)
- `-c, --column`: Column name containing tracking numbers (default: "Tracking Number")
- `-w, --workers`: Number of concurrent Chrome instances (default: 4)
- `-d, --delay`: Delay between requests in seconds (default: 2)
- `-m, --max`: Maximum items to process, 0 for all (default: 0)
- `--debug-dir`: Directory to save debug HTML files
- `--no-headless`: Disable headless mode (will show browser windows)

## Output Files

The script generates multiple output files:
- **results.csv**: Main CSV with tracking status for each number
- **results_events.csv**: Detailed tracking history events
- **results_report.html**: Friendly HTML report with all tracking details

## Comparison to PowerShell Version

This Python implementation offers several advantages over the PowerShell version:
- **Speed**: 5-10x faster by using concurrent processing
- **Reliability**: Better HTML parsing with Beautiful Soup
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Error handling**: More robust error detection and recovery
- **Debug capabilities**: Advanced HTML inspection and debugging

# ImageToText.ps1 Project

## Overview

This project automates the extraction of customer reference numbers from shipping label PDFs, generates barcodes for each reference, and merges those barcodes (with reference text) back onto the original PDF labels. It is designed for high-volume, batch processing of shipping labels (e.g., USPS/UPS pairs), ensuring that each label pair receives the correct reference and barcode.

**Key Features:**
- Extracts reference numbers (including hyphenated names) from PDFs using an OCR API
- Maintains strict label order and pairing (USPS/UPS)
- Generates Zint barcodes for each reference
- Merges barcodes and reference text onto both pages of each label pair
- Handles large batches (tested with 200+ labels)
- Robust error handling and retry logic for API failures

---

## Workflow

1. **PDF Input:**
   - User selects a PDF containing shipping labels (each pair = USPS + UPS).
2. **Text Extraction:**
   - The script sends the PDF (or its pages as images) to an OCR API.
   - Extracts customer reference numbers using advanced regex (supports hyphenated names).
   - Saves references to a CSV in the exact order of label pairs.
3. **Barcode Generation:**
   - Uses Zint to generate a barcode PNG for each reference (one per pair).
   - Barcodes are named to match their pair index for reliable mapping.
4. **PDF Merging:**
   - Uses PdfSharp to add a new section to each label page with:
     - "Reference 1" text
     - The extracted reference (e.g., `123456 Taylor-Jones`)
     - The corresponding barcode image
   - Both pages in a pair get the same reference/barcode.
5. **Output:**
   - Produces a new PDF with all barcodes and references correctly placed.

---

## Requirements

- **PowerShell 5+** (Windows recommended)
- **Zint** (barcode generator, Windows .exe)
- **PdfSharp.dll** (for PDF manipulation)
- **Ghostscript** (for PDF-to-image conversion, optional)
- **Internet access** (for OCR API)

---

## Setup

1. **Clone or copy the project files.**
2. **Install dependencies:**
   - Place `zint.exe` and `PdfSharp.dll` in the `Lib` directory or update the script paths.
   - Install Ghostscript if you want image-based PDF conversion.
3. **Configure script parameters:**
   - Edit the top of `ImageToText.ps1` to set paths for Zint, PdfSharp, and output folders if needed.

---

## Usage

Run the script in PowerShell:

```powershell
# Basic usage (will prompt for PDF)
./ImageToText.ps1

# Specify PDF and output folder
./ImageToText.ps1 -PdfPath "C:\path\to\labels.pdf" -OutputFolder "C:\path\to\Results"

# Specify Zint and PdfSharp paths if not in default location
./ImageToText.ps1 -ZintPath "C:\path\to\zint.exe" -PdfSharpPath "C:\path\to\PdfSharp.dll"
```

**After running:**
- Check the `Results` folder for:
  - `references.csv` (extracted references, in order)
  - `Barcodes` folder (barcode PNGs)
  - Merged PDF with barcodes and reference text

---

## Troubleshooting

### Common Issues

- **API 502/504 errors:**
  - The script now retries up to 3 times with increasing delay. If failures persist, check your internet connection or try again later.
- **No barcodes on output:**
  - Ensure Zint is installed and the path is correct.
  - Check that references were extracted (see `references.csv`).
- **Wrong reference/barcode on label:**
  - The script uses strict order and pairing logic. If you edited the CSV, ensure the order matches the label pairs.
- **Script crashes or missing dependencies:**
  - Make sure all required .exe and .dll files are present and paths are correct.
- **Hyphenated names not recognized:**
  - Regex patterns in the script support hyphens. If you find a missed case, check the debug output in the `Debug` folder.
- **Manual reference entry:**
  - If no references are found, the script will prompt for manual entry. Enter the 6-digit number and name as they appear on the label.

### Debugging Tips
- Check the `Debug` folder for per-page OCR text if extraction fails.
- Use the `Generate-BarcodesFromCSV` helper to visualize and debug barcode/reference mapping.
- Use `Write-Host` output for step-by-step progress and error messages.

---

## Reproducible Project Prompt

> **Prompt for Future Projects:**
>
> "I want a PowerShell script that takes a multi-page PDF of shipping labels (USPS/UPS pairs), extracts a customer reference number (6 digits + name, including hyphenated names) from each pair using OCR, generates a barcode for each reference, and merges the barcode and reference text back onto both pages of each pair in a new PDF. The script should:
> - Maintain strict label order and pairing
> - Save references to CSV in order
> - Use Zint for barcode generation
> - Use PdfSharp for PDF editing
> - Handle API errors with retries
> - Be robust for large batches (200+ labels)
> - Include debug output and troubleshooting guidance
> - Be easy to configure and run on Windows."

---

## Best Practices for Future Projects

- **Write a clear, detailed prompt before coding.**
- **Break down the workflow into steps and modules.**
- **Add debug output and error handling early.**
- **Document requirements and setup.**
- **Test with real data and edge cases (e.g., hyphenated names, large batches).**
- **Iterate and refactor for clarity and maintainability.**

---

*Happy automating!* # PHK-image-comparison-tool
