# SCX & PAK Extraction and Reinsertion Tools

This tool was created by **gopicolo** for extracting and reinserting text in the game *Di Gi Charat Fantasy*.

This repository contains two sets of Python scripts:
One set for working with .SCX text files (used in both Dreamcast and PS2 versions)
Another for handling .PAK archive files from the PS2 version

## 🧰 Scripts Included

### `dump.py` – Extract Text

This script reads `.SCX` files from the `input/` folder and extracts text blocks starting from the pointer table at offset `0x08`. It converts null bytes (`\x00`) into `<00>` tags for readability and saves the extracted text into `.txt` files in the `output/` folder.

**Features:**
- Automatically detects pointer tables.
- Converts binary strings to readable Shift-JIS text.
- Tags detected bytes like `<00>`, `<1F>`, etc.
- Saves all encountered tags to `found_tags.txt`.

### `inject.py` – Reinsert Text

This script reads the edited `.txt` files from `output/` and reinserts the modified text into the corresponding `.SCX` files. The resulting patched files are saved in the `modified/` folder.

**Features:**
- Reconstructs the pointer table based on the new text length.
- Supports `<00>` tags (converted back to null bytes).
- Ensures Shift-JIS encoding and null-terminated strings.

📦 Scripts for .PAK Files (PS2 Version)
The PAK/ folder contains scripts to extract and rebuild .PAK archives used in the PS2 version of Di Gi Charat Fantasy. These archives store binary resources like graphics, sounds, or sub-files.

extract.py – Extract .PAK Archives
Scans the input/ folder for all .PAK files.

Extracts each archive into a corresponding subfolder inside extracted/.

Automatically parses file tables, calculates offsets, and names extracted files properly.

repack.py – Repack .PAK Archives
Rebuilds .PAK files using the original archive as reference for file order and metadata.

Reads each folder in extracted/ and generates a new .PAK file in the repacked/ folder.

Keeps alignment to 2048-byte PS2 sector boundaries.

## 📁 Folder Structure

```
project/
├── input/         # Place your .SCX and .PAK files here
├── output/        # Extracted .txt files from SCX
├── modified/      # Repacked .SCX files
├── extracted/     # Extracted contents of .PAK files
├── repacked/      # Rebuilt .PAK files
├── dump.py        # SCX text extractor
├── inject.py      # SCX text reinserter
└── PAK/
    ├── extract.py # PAK archive extractor
    └── repack.py  # PAK archive rebuilder
```

## ✅ How to Use
For .SCX Files:
1. Place your `.SCX` files in the `input/` folder.
2. Run `dump.py` to extract text:
   ```bash
   python dump.py
   ```
3. Edit the text files in `output/`, keeping tags like `<00>` intact.
4. Run `inject.py` to rebuild `.SCX` files:
   ```bash
   python inject.py
   ```
For .PAK Files (PS2):
1. Place all .PAK files in input/
2. Run PAK/extract.py to extract
3. Modify contents inside extracted/ folders
4. Run PAK/repack.py to rebuild
 
## 📝 Notes

- The tool assumes that text pointers begin at offset `0x08` in the `.SCX` file.
- Text is encoded using **Shift-JIS**.
- You must preserve tag formatting when editing text (e.g., `<00>`).

## 🧪 Requirements

- Python 3.x

No additional libraries are required (uses only the Python standard library).
