from flask import send_from_directory
import os
from flask import Flask, request, jsonify
from figma_parser import parse_figma
from android_code_generator import generate_android_code
from build_manager import build_project

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    figma_file_id = data.get("figma_file_id")
    project_name = data.get("project_name", "GeneratedApp")

    semantic_json = parse_figma(figma_file_id)
    project_path = generate_android_code(semantic_json, project_name)
    apk_path = build_project(project_path)

    return jsonify({
        "success": True,
        "project_path": project_path,
        "apk_link": apk_path
    })

@app.route("/download/<project>/<filename>")
def download_file(project, filename):
    directory = os.path.join("outputs", project)
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
