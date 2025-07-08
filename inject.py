import os
import struct
import re

input_dir = 'input'
text_dir = 'output'
modified_dir = 'modified'

os.makedirs(modified_dir, exist_ok=True)

txt_files = [f for f in os.listdir(text_dir) if f.endswith('_extracted.txt')]
scx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.scx')]

print(f".SCX files found in input_dir: {scx_files}")
print(f".txt files found in text_dir: {txt_files}")

for txt_file in txt_files:
    base_name = txt_file[:-14]
    scx_file_name = base_name + '.SCX'

    if scx_file_name not in scx_files:
        print(f".SCX file not found for {txt_file}, skipping.")
        continue

    scx_path = os.path.join(input_dir, scx_file_name)
    txt_path = os.path.join(text_dir, txt_file)
    modified_path = os.path.join(modified_dir, scx_file_name)

    with open(scx_path, 'rb') as f:
        scx_data = bytearray(f.read())

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    # Coleta blocos de texto
    blocks = []
    current_block = []

    for line in lines:
        if line.startswith('# Pointer:'):
            if current_block:
                blocks.append(current_block)
                current_block = []
        current_block.append(line)

    if current_block:
        blocks.append(current_block)

    # Offset do primeiro texto
    if len(scx_data) < 0x0C:
        print(f"File {scx_file_name} too small to read pointer at 0x08, skipping.")
        continue
    first_text_offset = struct.unpack('<I', scx_data[0x08:0x0C])[0]

    new_text = bytearray()
    new_pointers = []

    for block in blocks:
        # Remove linha do ponteiro
        text_lines = [line for line in block if not line.startswith('# Pointer:')]
        if not text_lines:
            continue

        # Junta texto e processa tags <00>
        text_str = '\n'.join(text_lines).replace('<00>', '\x00')

        # Codifica em Shift-JIS
        sjis = text_str.encode('shift_jis', errors='ignore')

        # Garante terminador
        if not sjis.endswith(b'\x00'):
            sjis += b'\x00'

        pointer_value = first_text_offset + len(new_text)
        new_pointers.append(pointer_value)
        new_text += sjis

    # Reconstrói SCX
    out_data = bytearray(scx_data[:first_text_offset])

    pointer_offset = 0x08
    for ptr in new_pointers:
        out_data[pointer_offset:pointer_offset+4] = struct.pack('<I', ptr)
        pointer_offset += 4

    out_data += new_text

    with open(modified_path, 'wb') as f:
        f.write(out_data)

    print(f"Modified file saved: {modified_path}")

print("Reinsertion finished.")
