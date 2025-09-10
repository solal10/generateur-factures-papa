import os

def split_file(filename, chunk_size=1024*1024):  # 1MB chunks
    """Split a file into smaller chunks"""
    base_name = os.path.splitext(filename)[0]
    
    with open(filename, 'rb') as f:
        chunk_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            chunk_filename = f"{base_name}.part{chunk_num:03d}"
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            print(f"Created: {chunk_filename}")
            chunk_num += 1
    
    return chunk_num

def create_rebuild_script(base_name, num_chunks):
    """Create a script to rebuild the file"""
    script_content = f'''@echo off
echo Rebuilding {base_name}.exe...

copy /b '''
    
    for i in range(num_chunks):
        if i > 0:
            script_content += " + "
        script_content += f"{base_name}.part{i:03d}"
    
    script_content += f''' "{base_name}.exe"

echo Cleaning up temporary files...
'''
    
    for i in range(num_chunks):
        script_content += f'del "{base_name}.part{i:03d}"\n'
    
    script_content += f'\necho {base_name}.exe rebuilt successfully!'
    
    with open(f"rebuild_{base_name}.bat", 'w') as f:
        f.write(script_content)

if __name__ == "__main__":
    exe_path = "Generateur_Factures_Papa/FacturesGlobalSolutions.exe"
    if os.path.exists(exe_path):
        print(f"Splitting {exe_path}...")
        num_chunks = split_file(exe_path)
        create_rebuild_script("Generateur_Factures_Papa/FacturesGlobalSolutions", num_chunks)
        print(f"Split into {num_chunks} chunks")
        print("Created rebuild_FacturesGlobalSolutions.bat")
    else:
        print(f"File not found: {exe_path}")