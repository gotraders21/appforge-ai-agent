import requests

# Map Figma node types to Jetpack Compose components
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
    FIGMA_TOKEN = os.environ.get("FIGMA_TOKEN", "YOUR_FIGMA_TOKEN")
    url = f"https://api.figma.com/v1/files/{figma_file_id}"
    headers = {"X-Figma-Token": FIGMA_TOKEN}

    res = requests.get(url, headers=headers).json()

    if "document" not in res:
        raise ValueError("Invalid Figma response, missing 'document'")

    screens = []
    for frame in res['document']['children']:
        screen = {"name": frame['name'], "components": []}
        for node in frame.get('children', []):
            ctype = FIGMA_TO_COMPOSE.get(node['type'], "Text")
            label = node.get('name', '')
            action = None
            if ctype == "Button" and "navigate" in node.get('pluginData', ''):
                action = f"navigate:{node['pluginData']['navigate']}"
            screen['components'].append({"type": ctype, "label": label, "action": action})
        screens.append(screen)
    return {"screens": screens}
