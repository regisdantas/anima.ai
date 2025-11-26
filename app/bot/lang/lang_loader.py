import json

_language = None

def get_language():
    global _language
    
    if _language is None:
        with open("app/bot/lang/pt_BR.json", "r") as file:
            _language = json.load(file)

    return _language