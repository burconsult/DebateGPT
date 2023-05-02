import requests

# This function will return the client's IP address using the Abstract API (doesn't work on Streamlit Sharing)
def get_client_ip(api_key):
    try:
        response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}")
        result = response.json()
        ip = result['ip_address']
        return ip
    except:
        return None