import os
import shutil
from pathlib import Path

# Proje kaynak yolu (script'in bulunduğu klasör)
source_path = Path(__file__).parent

# Masaüstü hedef yolu
desktop_path = Path.home() / "Desktop" / "Document-Chatbot"

# Hariç tutulacak klasörler ve dosyalar
exclude_dirs = {'node_modules', '__pycache__', '.git', 'chroma_db', 'uploads', '.env'}
exclude_files = {'.env', 'create_zip.py', 'copy_to_desktop.py'}

print(f"Kaynak: {source_path}")
print(f"Hedef: {desktop_path}")

# Eğer hedef varsa sil
if desktop_path.exists():
    print("Eski klasör siliniyor...")
    shutil.rmtree(desktop_path)

# Klasörü oluştur
desktop_path.mkdir(parents=True, exist_ok=True)

# Dosyaları kopyala
copied_files = 0
copied_dirs = 0

for root, dirs, files in os.walk(source_path):
    # Hariç tutulacak klasörleri listeden çıkar
    dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
    
    # Göreceli yol
    rel_path = Path(root).relative_to(source_path)
    dest_dir = desktop_path / rel_path
    
    # Klasörü oluştur
    if rel_path != Path('.'):
        dest_dir.mkdir(parents=True, exist_ok=True)
        copied_dirs += 1
    
    # Dosyaları kopyala
    for file in files:
        if file not in exclude_files and not file.endswith(('.pyc', '.pyo')):
            src_file = Path(root) / file
            dest_file = dest_dir / file
            shutil.copy2(src_file, dest_file)
            copied_files += 1

print(f"\n✓ Kopyalama tamamlandı!")
print(f"  - {copied_dirs} klasör")
print(f"  - {copied_files} dosya")
print(f"\nProje masaüstünde: {desktop_path}")
