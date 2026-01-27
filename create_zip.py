import os
import zipfile
from pathlib import Path

# Proje yolu
project_path = Path(__file__).parent
zip_path = project_path.parent / "Document-Chatbot.zip"

# Hariç tutulacak klasörler ve dosyalar
exclude_patterns = [
    '__pycache__',
    '.git',
    'node_modules',
    'chroma_db',
    'uploads',
    '.env',
    '.pyc',
    '.pyo',
    '__pycache__',
    '.DS_Store',
    'Thumbs.db'
]

def should_exclude(file_path):
    """Dosyanın hariç tutulup tutulmayacağını kontrol et"""
    path_str = str(file_path)
    for pattern in exclude_patterns:
        if pattern in path_str:
            return True
    return False

# ZIP oluştur
print(f"Proje yolu: {project_path}")
print(f"ZIP yolu: {zip_path}")

if zip_path.exists():
    zip_path.unlink()
    print("Eski ZIP dosyası silindi")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_path):
        # Hariç tutulacak klasörleri listeden çıkar
        dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            if not should_exclude(file_path):
                arcname = file_path.relative_to(project_path)
                zipf.write(file_path, arcname)
                print(f"Eklendi: {arcname}")

print(f"\nZIP dosyası oluşturuldu: {zip_path}")
print(f"Boyut: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
