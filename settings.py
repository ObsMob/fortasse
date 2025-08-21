import json


def load_settings():
    with open("settings.json", "r") as f:
        settings_json = json.load(f)

    settings_py = {}
    for key, value in settings_json.items():
        if key == "TILE_SHAPE":
            settings_py[key] = getattr(TileShape, value)
        elif key == "RESOLUTION":
            settings_py[key] = getattr(Resolutions, value)
        else:
            settings_py[key] = value

    return settings_py

def save_settings(settings_py):
    settings_json = {}

    for key, value in settings_py.items():
        if isinstance(value, TileShape) or isinstance(value, Resolutions):
            settings_json[key] = value.name
        else:
            settings_json[key] = value

    with open("settings.json", "w") as f:
        json.dump(settings_json, f, indent=4)

def update_setting(key, value):
    settings[key] = value
    
    save_settings(settings)
