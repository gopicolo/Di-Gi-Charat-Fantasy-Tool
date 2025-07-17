import os
import struct

# --- Settings ---
input_folder = 'input'  # Folder containing all .PAK files
output_base_folder = 'extracted'  # Base folder for extracted content
# -----------------

def extract_digicharat_pak(pak_path, output_dir):
    """
    Extracts files from a .PAK archive used in 'Di Gi Charat Fantasy Excellent'.
    """
    print(f"Opening file: {pak_path}")

    try:
        with open(pak_path, 'rb') as f:
            magic = f.read(8)
            if magic != b'PAKFILE\x00':
                print("Error: 'PAKFILE' signature not found. Invalid or unsupported file.")
                return

            num_files = struct.unpack('>I', f.read(4))[0]
            print(f"Number of files: {num_files}")

            if num_files <= 0 or num_files > 5000:
                print("Suspicious number of files. Aborting.")
                return

            f.read(4)  # Skip padding

            # Read Table of Contents (TOC)
            file_entries = []
            print("Reading Table of Contents...")
            for _ in range(num_files):
                entry_data = f.read(64)
                if len(entry_data) < 64:
                    print("Warning: Unexpected end of file in TOC.")
                    break

                name_bytes, offset_sector, size = struct.unpack('>56sII', entry_data)
                name = name_bytes.split(b'\x00', 1)[0].decode('shift_jis', errors='ignore')
                offset = offset_sector * 2048
                file_entries.append({'name': name, 'offset': offset, 'size': size})

            os.makedirs(output_dir, exist_ok=True)
            print(f"Extracting to: {output_dir}")

            total_size = os.path.getsize(pak_path)
            for entry in file_entries:
                if not entry['name']:
                    print("Warning: Skipping unnamed file.")
                    continue

                if entry['offset'] + entry['size'] > total_size:
                    print(f"ERROR: File '{entry['name']}' exceeds archive size. Skipping.")
                    continue

                f.seek(entry['offset'])
                data = f.read(entry['size'])
                output_path = os.path.join(output_dir, entry['name'])

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as out_file:
                    out_file.write(data)

                print(f"  Extracted: {entry['name']} ({entry['size']} bytes)")

            print("Extraction complete!")

    except Exception as e:
        print(f"ERROR while processing '{pak_path}': {e}")

# Process all .PAK files in the input folder
if __name__ == '__main__':
    if not os.path.exists(input_folder):
        print(f"ERROR: Input folder '{input_folder}' not found.")
    else:
        pak_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pak')]
        if not pak_files:
            print("No .PAK files found in the input folder.")
        for pak_file in pak_files:
            pak_path = os.path.join(input_folder, pak_file)
            out_dir = os.path.join(output_base_folder, os.path.splitext(pak_file)[0])
            extract_digicharat_pak(pak_path, out_dir)
