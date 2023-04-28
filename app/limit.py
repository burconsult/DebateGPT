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

@limits(calls=3, period=ONE_HOUR)
def rate_limited_call(ip):
    pass

def is_rate_limited(ip):
    try:
        rate_limited_call(ip)
        return False
    except RateLimitException:
        return True