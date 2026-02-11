import os

def generate_android_project(blueprint, project_name):
    """
    Generates a full Android Studio project from blueprint JSON
    with navigation and ViewModels wired.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(base_dir, "outputs", project_name)

    # -------------------------------
    # 1. Create base directories
    app_src_dir = os.path.join(
        project_root, "app", "src", "main", "java", "com", "appforge", project_name.lower()
    )
    os.makedirs(app_src_dir, exist_ok=True)

    res_dir = os.path.join(project_root, "app", "src", "main", "res")
    os.makedirs(res_dir, exist_ok=True)

    # 2. Create viewmodel directory
    viewmodel_dir = os.path.join(app_src_dir, "viewmodels")
    os.makedirs(viewmodel_dir, exist_ok=True)

    # -------------------------------
    # 2. settings.gradle
    with open(os.path.join(project_root, "settings.gradle"), "w") as f:
        f.write(f"rootProject.name = '{project_name}'\ninclude ':app'")

    # 3. Root build.gradle
    with open(os.path.join(project_root, "build.gradle"), "w") as f:
        f.write("""
buildscript {
    ext {
        compose_version = '1.5.0'
    }
}
""")

    # 4. App build.gradle
    app_build_gradle = os.path.join(project_root, "app", "build.gradle")
    os.makedirs(os.path.dirname(app_build_gradle), exist_ok=True)
    with open(app_build_gradle, "w") as f:
        f.write("""
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.appforge.generated'
    compileSdk 34

    defaultConfig {
        applicationId "com.appforge.generated"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildFeatures {
        compose true
    }

    composeOptions {
        kotlinCompilerExtensionVersion '1.5.0'
    }
}

dependencies {
    implementation "androidx.core:core-ktx:1.12.0"
    implementation "androidx.activity:activity-compose:1.8.0"
    implementation "androidx.compose.ui:ui:1.5.0"
    implementation "androidx.compose.material:material:1.5.0"
    implementation "androidx.compose.ui:ui-tooling-preview:1.5.0"
    implementation "androidx.navigation:navigation-compose:2.7.3"
    implementation "androidx.lifecycle:lifecycle-viewmodel-compose:2.7.2"
}
""")

    # -------------------------------
    # 5. AndroidManifest.xml
    manifest_dir = os.path.join(project_root, "app", "src", "main")
    os.makedirs(manifest_dir, exist_ok=True)
    with open(os.path.join(manifest_dir, "AndroidManifest.xml"), "w") as f:
        f.write(f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="{project_name}"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

    # -------------------------------
    # 6. Generate screens + ViewModels
    screens = blueprint.get("screens", [])

    for screen in screens:
        screen_name = screen["name"]
        components = screen.get("components", [])

        # ---- Screen Kotlin File ----
        screen_file = os.path.join(app_src_dir, f"{screen_name}.kt")
        with open(screen_file, "w") as f:
            f.write(f"""
package com.appforge.{project_name.lower()}

import androidx.compose.material.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import com.appforge.{project_name.lower()}.viewmodels.{screen_name}ViewModel

@Composable
fun {screen_name}(navController: NavController, vm: {screen_name}ViewModel = viewModel()) {{
    MaterialTheme {{
        Surface {{
""")
            for comp in components:
                ctype = comp.get("type")
                label = comp.get("label", "")
                var_name = label.replace(" ", "_").lower()
                if ctype.lower() in ["textfield", "passwordfield"]:
                    f.write(f'            TextField(value = vm.{var_name}, onValueChange = {{ vm.{var_name} = it }}, label = {{ Text("{label}") }})\n')
                elif ctype.lower() == "button":
                    action = comp.get("action", "")
                    if action.startswith("navigate:"):
                        target = action.split(":")[1]
                        f.write(f'            Button(onClick = {{ navController.navigate("{target}") }}) {{ Text("{label}") }}\n')
                    else:
                        f.write(f'            Button(onClick = {{ /* TODO */ }}) {{ Text("{label}") }}\n')
                elif ctype.lower() == "text":
                    f.write(f'            Text("{label}")\n')
                elif ctype.lower() == "topappbar":
                    f.write(f'            TopAppBar(title = {{ Text("{comp.get("title","")}") }})\n')
                elif ctype.lower() == "cardlist":
                    f.write(f'            Text("CardList placeholder: {comp.get("source","")}")\n')

            f.write("""
        }}
    }}
}}

@Preview
@Composable
fun Preview{0}() {{
    {0}(navController = androidx.navigation.compose.rememberNavController())
}}
""".format(screen_name))

        # ---- ViewModel File ----
        vm_file = os.path.join(viewmodel_dir, f"{screen_name}ViewModel.kt")
        with open(vm_file, "w") as f:
            f.write(f"""
package com.appforge.{project_name.lower()}.viewmodels

import androidx.lifecycle.ViewModel
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

class {screen_name}ViewModel : ViewModel() {{
""")
            for comp in components:
                if comp["type"].lower() in ["textfield", "passwordfield"]:
                    var_name = comp["label"].replace(" ", "_").lower()
                    f.write(f'    var {var_name} by mutableStateOf("")\n')
            f.write("}\n")

    # -------------------------------
    # 7. Generate NavGraph.kt
    nav_graph_file = os.path.join(app_src_dir, "NavGraph.kt")
    with open(nav_graph_file, "w") as f:
        f.write(f"""
package com.appforge.{project_name.lower()}

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController

@Composable
fun NavGraph() {{
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "{screens[0]['name']}") {{
""")
        for screen in screens:
            screen_name = screen['name']
            f.write(f'        composable("{screen_name}") {{ {screen_name}(navController) }}\n')

        f.write("""
    }
}
""")

    # -------------------------------
    # 8. Generate MainActivity.kt
    main_activity_file = os.path.join(app_src_dir, "MainActivity.kt")
    with open(main_activity_file, "w") as f:
        f.write(f"""
package com.appforge.{project_name.lower()}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material.MaterialTheme

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            MaterialTheme {{
                NavGraph()
            }}
        }}
    }}
}}
""")

    return project_root
