def import_app():
    from app.application import Application
    return Application()

def validate_network_credentials(ssid, password):
    if len(ssid) > 32 or len(password) < 8:
        return False
    return True