import requests
from ratelimiter import RateLimiter

ip_rate_limiters = {}

def get_client_ip():
    try:
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        return ip
    except:
        return None
    
def is_rate_limited(ip):
    if ip not in ip_rate_limiters:
        ip_rate_limiters[ip] = RateLimiter(max_calls=3, period=3600)

    rate_limiter = ip_rate_limiters[ip]
    return not rate_limiter.call_allowed()

def get_rate_limit_remaining(ip):
    if ip not in ip_rate_limiters:
        ip_rate_limiters[ip] = RateLimiter(max_calls=3, period=3600)

    rate_limiter = ip_rate_limiters[ip]
    
    with rate_limiter:
        remaining_calls = rate_limiter.max_calls - len(rate_limiter.calls)
    return remaining_calls

def get_rate_limit_reset_time(ip):
    if ip not in ip_rate_limiters:
        ip_rate_limiters[ip] = RateLimiter(max_calls=3, period=3600)

    rate_limiter = ip_rate_limiters[ip]
    return rate_limiter.period_remaining()
