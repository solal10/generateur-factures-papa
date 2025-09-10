import zipfile
import os

def create_zip():
    # Create zip file
    zip_name = "Generateur_Factures_Papa.zip"
    folder_to_zip = "Generateur_Factures_Papa"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder and add all files
        for root, dirs, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip with relative path
                arcname = os.path.relpath(file_path, os.path.dirname(folder_to_zip))
                try:
                    zipf.write(file_path, arcname)
                    print(f"Added: {arcname}")
                except OSError as e:
                    print(f"Skipping {file_path}: {e}")
                    # Try copying the file first
                    import shutil
                    temp_file = file + "_temp"
                    temp_path = os.path.join(root, temp_file)
                    try:
                        shutil.copy2(file_path, temp_path)
                        zipf.write(temp_path, arcname)
                        os.remove(temp_path)
                        print(f"Added (via copy): {arcname}")
                    except Exception as e2:
                        print(f"Failed to add {file_path}: {e2}")
    
    print(f"\nZip file created successfully: {zip_name}")
    print(f"Size: {os.path.getsize(zip_name)} bytes")

if __name__ == "__main__":
    create_zip()