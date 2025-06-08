#----------------------------------------------------------------------
# requests_tools.py
#
# Functions for HTTP requests with error handling and retries.
# ---------------------------------------------------------------------

# Standard library imports - built-in modules that come with Python
import logging

# External libraries installed via pip
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Local libraries : project-specific modules
from log_config import logger  # Centralized logger


def make_requests(url, timeout=5, max_retries=3, backoff_factor=0.5):
    """
    Perform an HTTP GET request to the specified URL with retry and timeout handling.

    - Retries up to 'max_retries' times if the server returns certain error codes (e.g. 500, 503).
    - Waits longer between each retry (controlled by 'backoff_factor').
    - Logs warnings and returns None in case of errors.
    - Returns the response object if the request succeeds (status code 200-299).

    This function improves the resilience of web scraping or API access when network/server issues occur.
    """

    # Create a requests session (to reuse connections and apply settings)
    session = requests.Session()

    # Configure a retry strategy:
    # - total: max number of retries
    # - backoff_factor: time between retries (exponential)
    # - status_forcelist: list of HTTP codes that should trigger a retry
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        # Retry on these server errors
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],
        # Retry only for safe methods
        allowed_methods=[
            "HEAD",
            "GET",
            "OPTIONS",
        ],
    )

    # Create an adapter using this retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Mount the adapter to handle both HTTP and HTTPS
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        # Attempt the GET request with a timeout
        response = session.get(url, timeout=timeout)
    except requests.exceptions.RequestException as e:
        # Log any network-related error (timeout, connection, etc.)
        logger.warning(f"Request failed for URL {url}: {e}")
        return None

    # If response status is not OK (i.e. not in 200–299 range), log it
    if not response.ok:
        logger.warning(f"Request failed for URL {url} with status code {response.status_code}")
        return None

    # Return the successful response
    return response




