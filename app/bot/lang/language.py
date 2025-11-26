import json

_language = {}

def get_language():
    global _language
    
    if not _language:
        with open("app/bot/lang/pt_BR.json", "r") as file:
            _language = {}
            _language['pt_BR'] = json.load(file)

    return _language

def get_text(lang_code: str, key: str) -> str:
    language = get_language().get(lang_code, {})

    current = language
    for part in key.split("."):
        current = current.get(part, {})

    return current if isinstance(current, str) else ""

