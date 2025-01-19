import socket
import requests
import time

def check_ping(url):
    """
    Checks the latency and status of a given URL.

    Args:
        url (str): The URL to ping.

    Returns:
        dict: A dictionary containing the latency in milliseconds, HTTP status code, 
              IP address, domain, and the original URL. If an error occurs, 
              returns a dictionary with an 'error' key and the error message.
    """
    try:
        domain = url.replace("http://", "").replace("https://", "").split('/')[0]
        ip_address =socket.gethostbyname(domain)

        start_time = time.time()
        r = requests.get(url)
        latency = round((time.time() - start_time) * 1000, 2)
        
        status = r.status_code

        result = {
            "latency": f"{latency} ms",
            "status": status,
            "ip": ip_address,
            "domain": domain,
            "url": url,
        }
        return result
    except Exception as e:
        return {"error": str(e)}
