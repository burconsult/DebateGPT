from streamlit_javascript import st_javascript

# Get the user IP address
def client_ip():

    url = 'https://api.ipify.org?format=json'

    script = (f'await fetch("{url}").then('
                'function(response) {'
                    'return response.json();'
                '})')

    try:
        result = st_javascript(script)

        if isinstance(result, dict) and 'ip' in result:
            return result['ip']

    except:
        pass