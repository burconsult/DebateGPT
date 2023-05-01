import requests
import json
from ratelimit import limits, RateLimitException

ip_rate_limiters = {}

def get_client_ip(api_key):
    try:
        response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}")
        result = json.loads(response.content)
        ip = str(format(result['ip_address']))
        return ip
    except:
        return None

ONE_HOUR = 3600

@limits(calls=10, period=ONE_HOUR)
def rate_limited_call(ip):
    pass


def is_rate_limited(ip):

    # Check if the IP address is on the whitelist
    if ip == 'admin':
        return False

    # Continue with the rate limit check
    try:
        rate_limited_call(ip)
        return False
    except RateLimitException:
        return True