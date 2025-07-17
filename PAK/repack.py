import os
import struct

# --- Settings ---
extracted_base_folder = 'extracted'
original_pak_folder = 'input'
output_pak_folder = 'repacked'
# ----------------

def repack_digicharat_pak(input_dir, original_pak_path, new_pak_path):
    """
    Rebuilds a .PAK archive from extracted files.
    """
    print(f"\nReading file order from: {original_pak_path}")

    if not os.path.exists(original_pak_path):
        print(f"ERROR: Original .PAK file '{original_pak_path}' not found.")
        return

    if not os.path.exists(input_dir):
        print(f"ERROR: Input folder '{input_dir}' not found.")
        return

    try:
        with open(original_pak_path, 'rb') as f_orig:
            f_orig.read(8)  # Skip 'PAKFILE\x00'
            num_files = struct.unpack('>I', f_orig.read(4))[0]
            f_orig.read(4)  # Skip padding

            original_file_names = []
            for _ in range(num_files):
                entry_data = f_orig.read(64)
                name_bytes, _, _ = struct.unpack('>56sII', entry_data)
                name = name_bytes.split(b'\x00', 1)[0].decode('shift_jis', errors='ignore')
                if name:
                    original_file_names.append(name)

        with open(new_pak_path, 'wb') as f_new:
            print(f"Creating new PAK: {new_pak_path}")

            f_new.write(b'PAKFILE\x00')
            f_new.write(struct.pack('>I', len(original_file_names)))
            f_new.write(b'\x00\x00\x00\x00')  # Padding

            toc_size = len(original_file_names) * 64
            f_new.write(bytearray(toc_size))

            SECTOR_SIZE = 2048
            current_offset = 16 + toc_size
            pad = (SECTOR_SIZE - (current_offset % SECTOR_SIZE)) % SECTOR_SIZE
            f_new.write(b'\x00' * pad)
            current_offset += pad

            new_entries = []

            for filename in original_file_names:
                path = os.path.join(input_dir, filename)
                if not os.path.exists(path):
                    print(f"WARNING: '{filename}' not found in input. Skipping.")
                    continue

                with open(path, 'rb') as f_in:
                    data = f_in.read()
                    size = len(data)
                    offset_sector = current_offset // SECTOR_SIZE

                    new_entries.append({
                        'name': filename,
                        'offset_sector': offset_sector,
                        'size': size
                    })

                    f_new.write(data)
                    print(f"  -> Added: {filename} ({size} bytes)")

                    current_offset += size
                    pad = (SECTOR_SIZE - (current_offset % SECTOR_SIZE)) % SECTOR_SIZE
                    f_new.write(b'\x00' * pad)
                    current_offset += pad

            f_new.seek(16)
            for entry in new_entries:
                name_bytes = entry['name'].encode('shift_jis', errors='ignore')
                padded_name = name_bytes.ljust(56, b'\x00')
                toc_entry = struct.pack('>56sII', padded_name, entry['offset_sector'], entry['size'])
                f_new.write(toc_entry)

        print(f"Repacked successfully: {new_pak_path}")

    except Exception as e:
        print(f"ERROR while repacking '{new_pak_path}': {e}")

# Process all extracted folders
if __name__ == '__main__':
    if not os.path.exists(extracted_base_folder):
        print(f"ERROR: Extracted folder '{extracted_base_folder}' not found.")
    else:
        os.makedirs(output_pak_folder, exist_ok=True)
        for folder in os.listdir(extracted_base_folder):
            input_dir = os.path.join(extracted_base_folder, folder)
            original_pak = os.path.join(original_pak_folder, f"{folder}.PAK")
            new_pak = os.path.join(output_pak_folder, f"{folder}_NEW.PAK")
            repack_digicharat_pak(input_dir, original_pak, new_pak)
