import os
import zipfile

def zip_project(project_path: str, outputs_dir: str) -> str:
    """
    Zip the generated Android project into the outputs folder
    """
    os.makedirs(outputs_dir, exist_ok=True)
    zip_name = os.path.join(outputs_dir, os.path.basename(project_path) + ".zip")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                abs_path = os.path.join(root, file)
                # relative path inside zip
                rel_path = os.path.relpath(abs_path, os.path.dirname(project_path))
                zipf.write(abs_path, rel_path)

    return zip_name
