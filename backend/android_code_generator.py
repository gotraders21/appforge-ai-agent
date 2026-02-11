import os

def generate_android_project(semantic_json, project_name):
    """
    Generates basic Android project structure.
    """

    base_path = os.path.join("outputs", project_name)
    os.makedirs(base_path, exist_ok=True)

    app_path = os.path.join(base_path, "app")
    os.makedirs(app_path, exist_ok=True)

    main_activity = f"""
package com.appforge.{project_name.lower()}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            Text("Hello from AppForge AI")
        }}
    }}
}}
"""

    with open(os.path.join(app_path, "MainActivity.kt"), "w") as f:
        f.write(main_activity)

    return base_path
