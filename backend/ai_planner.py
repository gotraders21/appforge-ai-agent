import re

def generate_blueprint(user_prompt):
    """
    Mock AI Planner.
    Converts simple app descriptions into structured blueprint JSON.
    """

    prompt = user_prompt.lower()

    screens = []
    navigation = []

    # Basic detection rules
    if "login" in prompt:
        screens.append({
            "name": "LoginScreen",
            "components": [
                {"type": "TextField", "label": "Email"},
                {"type": "PasswordField", "label": "Password"},
                {"type": "Button", "label": "Login", "action": "navigate:HomeScreen"}
            ]
        })

    if "dashboard" in prompt or "home" in prompt:
        screens.append({
            "name": "HomeScreen",
            "components": [
                {"type": "TopAppBar", "title": "Home"},
                {"type": "Text", "label": "Welcome to your app"}
            ]
        })

    if len(screens) > 1:
        navigation.append({
            "from": screens[0]["name"],
            "to": screens[1]["name"]
        })

    blueprint = {
        "app_name": "GeneratedApp",
        "theme": "Material3",
        "screens": screens,
        "navigation": navigation,
        "state_management": "ViewModel"
    }

    return blueprint
