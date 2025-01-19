import socket
import requests
import time

def check_ping(url):
    try:
        # Extract domain from URL
        domain = url.replace("http://", "").replace("https://", "").split('/')[0]
        ip_address = socket.gethostbyname(domain)
        
        # Measure latency
        start_time = time.time()
        response = requests.get(url)
        latency = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
        
        # Get status
        status = response.status_code
        
        # Create result dictionary
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

# Example usage
url = "https://discord.com/"
result = check_ping(url)
print(result)
