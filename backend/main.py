import os
import re
from flask import Flask, request, jsonify, send_from_directory
from figma_parser import parse_figma
from android_code_generator import generate_android_project
from build_manager import zip_project

app = Flask(__name__)

def extract_figma_file_id(figma_url: str) -> str:
    """
    Extract Figma file ID from /file/<id>/ or /design/<id>/ URL
    """
    match = re.search(r"/(file|design)/([a-zA-Z0-9]+)", figma_url)
    if not match:
        raise ValueError("Invalid Figma URL format")
    return match.group(2)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Inputs from Lovable frontend
        user_prompt = request.json.get("user_prompt", "")
        figma_url = request.json.get("figma_url")
        project_name = request.json.get("project_name", "GeneratedApp")

        if not figma_url:
            return jsonify({"success": False, "error": "Figma URL is required"}), 400

        # Extract Figma file ID
        figma_file_id = extract_figma_file_id(figma_url)

        # Parse Figma → blueprint JSON
        blueprint = parse_figma(figma_file_id)

        # Generate Android Studio project
        project_path = generate_android_project(blueprint, project_name)

        # Zip the project
        zip_path = zip_project(project_path)

        return jsonify({
            "success": True,
            "download_link": f"/download_file/{os.path.basename(zip_path)}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/download_file/<filename>")
def download_file(filename):
    outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../outputs")
    return send_from_directory(outputs_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
