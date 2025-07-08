Di Gi Charat Fantasy Text Extraction and Reinsertion Tools
This repository contains two Python scripts designed to extract and reinsert Shift-JIS encoded text from .SCX files, used in Di Gi Charat Fantasy
works with both the Dreamcast and PS2 versions.

🧰 Scripts Included
dump.py – Extract Text
This script reads .SCX files from the input/ folder and extracts text blocks starting from the pointer table at offset 0x08. It converts null bytes (\x00) into <00> tags for readability and saves the extracted text into .txt files in the output/ folder.

Features:

Automatically detects pointer tables.

Converts binary strings to readable Shift-JIS text.

Tags detected bytes like <00>, <1F>, etc.

Saves all encountered tags to found_tags.txt.

inject.py – Reinsert Text
This script reads the edited .txt files from output/ and reinserts the modified text into the corresponding .SCX files. The resulting patched files are saved in the modified/ folder.

Features:

Reconstructs the pointer table based on the new text length.

Supports <00> tags (converted back to null bytes).

Ensures Shift-JIS encoding and null-terminated strings.

📁 Folder Structure
graphql
Copiar
Editar
project/
├── input/       # Original .SCX files
├── output/      # Extracted .txt files (also where you edit the text)
├── modified/    # Output patched .SCX files
├── dump.py      # Extract script
└── inject.py    # Reinsert script
✅ How to Use
Place your .SCX files in the input/ folder.

Run dump.py to extract text:

bash
Copiar
Editar
python dump.py
Edit the text files in output/, keeping tags like <00> intact.

Run inject.py to rebuild .SCX files:

bash
Copiar
Editar
python inject.py
📝 Notes
The tool assumes that text pointers begin at offset 0x08 in the .SCX file.

Text is encoded using Shift-JIS.

You must preserve tag formatting when editing text (e.g., <00>).

🧪 Requirements
Python 3.x

No additional libraries are required (uses only the Python standard library).
