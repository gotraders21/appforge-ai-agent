import os
import shutil

TEMPLATE_PATH = '../android_template'

def generate_kotlin_project(project_name, semantic_json):
    output_path = os.path.join('outputs/generated_project', project_name)
    os.makedirs(output_path, exist_ok=True)

    shutil.copytree(TEMPLATE_PATH, output_path, dirs_exist_ok=True)

    screens_path = os.path.join(output_path, 'app/src/main/java/com/appforge/screens')
    os.makedirs(screens_path, exist_ok=True)

    for screen in semantic_json['screens']:
        file_name = f"{screen['name'].replace(' ', '_')}.kt"
        with open(os.path.join(screens_path, file_name), 'w') as f:
            components_code = ""
            for comp in screen['components']:
                if comp['type'] == 'TEXT':
                    components_code += f'Text("{comp["name"]}")\n'
                elif comp['type'] == 'RECTANGLE':
                    components_code += 'Box(modifier = Modifier.size(100.dp))\n'
            f.write(f'''package com.appforge.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun {screen["name"].replace(" ", "_")}() {{
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {{
        {components_code}
    }}
}}
''')
    apk_link = f'{output_path}/app-debug.apk'
    return output_path, apk_link
