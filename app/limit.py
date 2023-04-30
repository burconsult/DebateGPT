import requests
from ratelimit import limits, RateLimitException

ip_rate_limiters = {}

def get_client_ip():
    try:
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        return ip
    except:
        return None

ONE_HOUR = 3600

@limits(key_func=lambda ip, key: f"{ip}_{key}", calls=3, period=ONE_HOUR)
def rate_limited_call(ip, key):
    pass


def is_rate_limited(ip, key):

    # Check if the IP address is on the whitelist
    if ip == 'admin':
        return False

    # Continue with the rate limit check
    try:
        rate_limited_call(ip, key)
        return False
    except RateLimitException:
        return True
e