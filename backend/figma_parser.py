def parse_figma(file_id):
    """
    MVP-safe parser.
    Prevents crashes if Figma API is unavailable.
    """

    if not file_id:
        file_id = "demo"

    # Temporary intelligent mock
    return {
        "app_name": "AppForge Generated App",
        "screens": [
            {
                "name": "LoginScreen",
                "components": [
                    {"type": "TEXT", "value": "Welcome Back"},
                    {"type": "INPUT", "value": "Email"},
                    {"type": "INPUT", "value": "Password"},
                    {"type": "BUTTON", "value": "Login"}
                ]
            },
            {
                "name": "HomeScreen",
                "components": [
                    {"type": "TEXT", "value": "Dashboard"},
                    {"type": "CARD", "value": "Analytics"},
                    {"type": "CARD", "value": "Settings"}
                ]
            }
        ]
    }
