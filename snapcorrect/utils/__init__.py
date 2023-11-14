import secrets

def generate_random_filename(extension):
    random_name = secrets.token_hex(8)
    return f"{random_name}.{extension}"
