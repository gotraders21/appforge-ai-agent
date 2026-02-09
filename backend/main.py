from flask import Flask, request, jsonify
from figma_parser import parse_figma
from code_generator import generate_kotlin_project

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    figma_file_id = data.get('figma_file_id')
    project_name = data.get('project_name', 'GeneratedApp')

    semantic_json = parse_figma(figma_file_id)
    project_path, apk_link = generate_kotlin_project(project_name, semantic_json)

    return jsonify({
        'success': True,
        'project_path': project_path,
        'apk_link': apk_link
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
