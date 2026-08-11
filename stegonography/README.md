# LSB Steganography Capacity Validator

This project implements a **pre-validation tool** for Least Significant Bit (LSB)
steganography. The goal of the program is to determine whether a chosen carrier
image has sufficient capacity to store a hidden file before any embedding logic
is applied.

## Overview

LSB steganography relies on modifying the least significant bit of each byte in
a carrier file (commonly an image) to embed hidden data. Because each byte can
store at most one bit using this method, it is important to validate capacity
before attempting to embed data.

This script performs that validation step by:
- Converting the hidden file into a bitstream
- Measuring the carrier file’s byte capacity
- Verifying whether the carrier can store the hidden data under a 1-bit-per-byte
  LSB model

No steganographic embedding is performed in this program.

## Features

- Binary-safe file handling
- Bit-level conversion of hidden data
- Capacity comparison using a standard LSB assumption
- Optional debug output for development and testing
- Modular structure supporting future embedding and extraction logic

## Design Philosophy

This project intentionally separates **validation**, **embedding**, and
**extraction** into distinct components. Performing a capacity check prior to
embedding prevents data corruption and allows steganographic operations to fail
safely.

The `embed_lsb()` and `extract_lsb()` functions are currently implemented as
stubs to define program structure and future expansion.

## Assumptions

- One bit of hidden data is stored per carrier byte (1 LSB per byte)
- Files are processed in raw binary form
- This tool is designed for educational and research purposes

## Limitations

- No embedding or extraction logic is implemented
- No error handling for invalid file paths
- Capacity validation only applies to a basic LSB model

## Future Work

- Implement LSB embedding using bit masking
- Implement extraction and reconstruction of hidden data
- Support dynamic file input via command-line arguments
- Improve error handling and input validation

## Usage

Edit the file paths in the main function:

```python
file_data = "hidden_file.jpg"
carrier_file = "carrier_image.jpg"
