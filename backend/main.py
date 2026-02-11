import os
from ai_planner import generate_blueprint
from flask import Flask, request, jsonify, send_from_directory
from figma_parser import parse_figma
from android_code_generator import generate_android_code
from build_manager import build_project

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_prompt = data.get("prompt")
    project_name = data.get("project_name", "GeneratedApp")

    blueprint = generate_blueprint(user_prompt)

    project_path = generate_android_project(blueprint, project_name)

    zip_path = build_project(project_name)

    return jsonify({
        "success": True,
        "zip_link": f"/download/{project_name}.zip"
    })


@app.route("/download/<project>/<filename>")
def download_file(project, filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(base_dir, "outputs", project)

    return send_from_directory(outputs_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
