import requests

FIGMA_API_KEY = 'YOUR_FIGMA_KEY'  # Replace with your Figma API key

def parse_figma(file_id):
    url = f'https://api.figma.com/v1/files/{file_id}'
    headers = {'X-Figma-Token': FIGMA_API_KEY}
    res = requests.get(url, headers=headers).json()

    screens = []
    for node in res['document']['children']:
        if node['type'] == 'CANVAS':
            for frame in node.get('children', []):
                screen_data = {
                    'id': frame['id'],
                    'name': frame['name'],
                    'type': frame['type'],
                    'components': []
                }
                for comp in frame.get('children', []):
                    if comp['type'] in ['TEXT', 'RECTANGLE', 'FRAME']:
                        screen_data['components'].append({
                            'id': comp['id'],
                            'name': comp.get('name', comp['type']),
                            'type': comp['type']
                        })
                screens.append(screen_data)
    return {'screens': screens}
