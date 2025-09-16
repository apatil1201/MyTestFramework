import logging
LOGGER = logging.getLogger("tests")


def log_response(resp):
    """Log API response details for debugging"""
    LOGGER.info(f"Status: {resp.status_code}")
    LOGGER.info(f"Response: {resp.json()}")