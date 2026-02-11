import os
from flask import Flask, request, jsonify, send_from_directory
from figma_parser import parse_figma
from android_code_generator import generate_android_project
from build_manager import zip_project

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Get inputs from Lovable frontend
        user_prompt = request.json.get("user_prompt", "")
        figma_url = request.json.get("figma_url")
        project_name = request.json.get("project_name", "GeneratedApp")

        if not figma_url:
            return jsonify({"success": False, "error": "Figma URL is required"}), 400

        # Extract Figma file ID from URL
        if "/file/" not in figma_url:
            return jsonify({"success": False, "error": "Invalid Figma URL"}), 400
        figma_file_id = figma_url.split("/file/")[1].split("/")[0]

        # Parse Figma → blueprint
        blueprint = parse_figma(figma_file_id)

        # Generate Android project
        project_path = generate_android_project(blueprint, project_name)

        # Zip the project for download
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
