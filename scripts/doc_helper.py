import os
import shutil
from datetime import datetime

def save_and_archive(doc, canonical_path):
    """
    Ensures docs/ directory has only the single canonical file.
    Whenever a new version is saved, any existing version is automatically
    moved into the docs/prev/ folder with a timestamp.
    """
    directory = os.path.dirname(canonical_path)
    filename = os.path.basename(canonical_path)
    base_name, ext = os.path.splitext(filename)
    
    prev_dir = os.path.join(directory, "prev")
    os.makedirs(prev_dir, exist_ok=True)
    
    if os.path.exists(canonical_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_filename = f"{base_name}_prev_{timestamp}{ext}"
        archived_path = os.path.join(prev_dir, archived_filename)
        try:
            shutil.move(canonical_path, archived_path)
            print(f"Previous version archived to: {archived_path}")
        except PermissionError:
            print(f"WARNING: '{canonical_path}' is open in Microsoft Word.")
            print("Please close it in Microsoft Word to allow archival.")
            # Fallback save into prev directory as a draft if locked
            draft_path = os.path.join(prev_dir, f"{base_name}_draft_{timestamp}{ext}")
            doc.save(draft_path)
            print(f"Draft saved to: {draft_path}")
            return draft_path

    doc.save(canonical_path)
    print(f"Canonical document saved to: {canonical_path}")
    return canonical_path
