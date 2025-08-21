import os
import glob

def cleanup_folder(folder_path, max_files=100):

    files= sorted(
        glob.glob(os.path.join(folder_path, "*")),
        key= os.path.getmtime
    )

    if len(files) > max_files:
        old_files= files[:len(files)- max_files]
        for f in old_files:
            try:
                os.remove(f)
                print(f"[CLEANUP] Removed old files")
            except Exception as e:
                print(f"[ERROR] Could not delete {f}: {e}")