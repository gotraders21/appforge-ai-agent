import os
import requests

FIGMA_TO_COMPOSE = {
    "TEXT": "Text",
    "BUTTON": "Button",
    "INPUT": "TextField",
    "PASSWORD": "PasswordField",
    "TOP_APP_BAR": "TopAppBar",
    "CARD": "Card",
    "IMAGE": "Image",
    "LIST": "LazyColumn"
}

def parse_figma(figma_file_id):
    """
    Parse Figma file and convert to blueprint JSON
    """
    FIGMA_TOKEN = os.environ.get("FIGMA_TOKEN")
    if not FIGMA_TOKEN:
        raise ValueError("FIGMA_TOKEN not set in environment variables")

    url = f"https://api.figma.com/v1/files/{figma_file_id}"
    headers = {"X-Figma-Token": FIGMA_TOKEN}
    res = requests.get(url, headers=headers).json()

    if "document" not in res:
        raise ValueError(f"Invalid Figma response: {res}")

    screens = []
    for frame in res['document'].get('children', []):
        screen = {"name": frame.get('name', 'Screen'), "components": []}
        for node in frame.get('children', []):
            ctype = FIGMA_TO_COMPOSE.get(node.get('type', 'TEXT'), 'Text')
            label = node.get('name', '')
            action = None
            if ctype == "Button" and "navigate" in node.get('pluginData', ''):
                action = f"navigate:{node['pluginData']['navigate']}"
            screen['components'].append({"type": ctype, "label": label, "action": action})
        screens.append(screen)

    if not screens:
        raise ValueError("No screens found in Figma file")
    return {"screens": screens}
