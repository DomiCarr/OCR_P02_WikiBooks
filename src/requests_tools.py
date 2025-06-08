import logging
import requests

logger = logging.getLogger(__name__)

def make_requests(url, timeout=5):
    """
    Perform a GET request to the given URL and return the response object.
    Generate a warning et return None if exception
    """
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed for URL {url}: {e}")
        return None  # Return None if an exception occurred during the request

    # Check if the HTTP response status is OK (status code 200-299)
    if not response.ok:
        logger.warning(f"Request failed for URL {url} with status code {response.status_code}")
        return None  # Return None if the response status indicates failure

    return response
