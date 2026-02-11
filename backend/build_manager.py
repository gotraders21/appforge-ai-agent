import os
import zipfile

def zip_project(project_path: str) -> str:
    """
    Zip the generated Android project for download
    """
    zip_name = f"{project_path}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, os.path.dirname(project_path))
                zipf.write(abs_path, rel_path)
    return zip_name
