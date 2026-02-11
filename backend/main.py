import os
from flask import Flask, request, jsonify, send_from_directory
from figma_parser import parse_figma
from android_code_generator import generate_android_code
from build_manager import build_project

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No JSON body provided"}), 400

    figma_file_id = data.get("figma_file_id")
    project_name = data.get("project_name", "GeneratedApp")

    if not figma_file_id:
        return jsonify({"success": False, "error": "Missing figma_file_id"}), 400

    # Parse Figma
    semantic_json = parse_figma(figma_file_id)

    # Generate Android project
    project_path = generate_android_code(semantic_json, project_name)

    # Build APK
    apk_path = build_project(project_path)

    return jsonify({
        "success": True,
        "apk_link": f"/download/{project_name}/app-debug.apk"
    })


@app.route("/download/<project>/<filename>")
def download_file(project, filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(base_dir, "outputs", project)

    return send_from_directory(outputs_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
