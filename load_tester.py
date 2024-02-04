import time
import requests
from concurrent.futures import ThreadPoolExecutor

def send_request(url):
    start_time = time.time()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return time.time() - start_time
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def load_test(url, num_requests, num_workers):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = (executor.submit(send_request, url) for _ in range(num_requests))
        times = [f.result() for f in futures if f.result() is not None]

    if times:
        print(f"Sent {num_requests} requests to {url} in parallel, using {num_workers} workers.")
        print(f"Average response time: {sum(times) / len(times)} seconds")
    else:
        print("No successful requests.")

# Example usage:
load_test("http://example.com", num_requests=100, num_workers=10)
