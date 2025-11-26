

def split_message(text, max_len=4096):
    parts = []
    current = ""

    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) + 2 <= max_len:
            current += paragraph + "\n\n"
        else:
            if current:
                parts.append(current.strip())
            current = paragraph + "\n\n"

    if current:
        parts.append(current.strip())

    return parts
