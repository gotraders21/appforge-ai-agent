import os
from flask import Flask, request, jsonify, send_from_directory
from figma_parser import parse_figma
from android_code_generator import generate_android_project
from build_manager import zip_project

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    # Get user prompt from frontend (Lovable dashboard)
    user_prompt = request.json.get("user_prompt", "")
    figma_file_id = request.json.get("figma_file_id")
    project_name = request.json.get("project_name", "GeneratedApp")

    if not figma_file_id:
        return jsonify({"success": False, "error": "Figma file ID required"}), 400

    # 1️⃣ Parse Figma file → blueprint JSON
    blueprint = parse_figma(figma_file_id)

    # 2️⃣ Generate Android Studio project (screens + ViewModels + navigation)
    project_path = generate_android_project(blueprint, project_name)

    # 3️⃣ Zip project for download
    zip_path = zip_project(project_path)

    return jsonify({
        "success": True,
        "download_link": f"/download_file/{os.path.basename(zip_path)}"
    })

@app.route("/download_file/<filename>")
def download_file(filename):
    outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../outputs")
    return send_from_directory(outputs_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
