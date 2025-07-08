import os
import re
from pathlib import Path

input_dir = 'input'
output_dir = 'output'
tags_file = os.path.join(output_dir, 'found_tags.txt')

os.makedirs(output_dir, exist_ok=True)

scx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.scx')]
tags_encontradas = set()

# Regex para encontrar qualquer tag do tipo <00>, <1F>, etc.
tag_pattern = re.compile(r'<[0-9A-Fa-f]{2}>')

for scx_file in scx_files:
    scx_path = os.path.join(input_dir, scx_file)
    out_path = os.path.join(output_dir, f"{Path(scx_file).stem}_extracted.txt")

    with open(scx_path, 'rb') as f:
        scx_data = f.read()

    size = len(scx_data)
    offset = 0x08
    pointers = []
    last_ptr = -1

    while offset + 4 <= size:
        ptr = int.from_bytes(scx_data[offset:offset+4], 'little')

        if ptr == 0 or ptr >= size:
            break
        if ptr < last_ptr:
            print(f"Pointer 0x{ptr:04X} smaller than previous 0x{last_ptr:04X} at offset 0x{offset:04X}. Stopping pointer reading.")
            break

        pointers.append(ptr)
        last_ptr = ptr
        offset += 4

    pointers.append(size)

    with open(out_path, 'w', encoding='utf-8') as out:
        for i in range(len(pointers) - 1):
            p1 = pointers[i]
            p2 = pointers[i + 1]
            block = scx_data[p1:p2]

            has_final_null = block.endswith(b'\x00')
            if has_final_null:
                block_core = block[:-1]
            else:
                block_core = block

            # Substituir todos os \x00 por <00> para visualização
            marked_bytes = block_core.replace(b'\x00', b'<00>')

            try:
                text = marked_bytes.decode('shift_jis', errors='ignore')
            except UnicodeDecodeError:
                text = f"[ERROR DECODING BLOCK {p1:04X}-{p2:04X}]"

            if has_final_null:
                text += '\x00'

            # Encontrar todas as tags <xx> e adicionar ao conjunto
            tags_encontradas.update(tag_pattern.findall(text))

            out.write(f"# Pointer: 0x{p1:04X}\n{text}")

            if i < len(pointers) - 2:
                out.write('\n')

    print(f"{scx_file} -> {out_path}")

# Salvar tags encontradas
with open(tags_file, 'w', encoding='utf-8') as f:
    for tag in sorted(tags_encontradas):
        f.write(f"{tag}\n")

print("Dump finished. Tags salvas em 'found_tags.txt'.")
