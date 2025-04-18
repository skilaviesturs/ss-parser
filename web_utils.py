import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    """Fetch the HTML content of the given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_html(html):
    """Parse HTML content using BeautifulSoup and return the soup object."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def fetch_and_parse(url):
    """Fetch a URL and return its BeautifulSoup object."""
    html = fetch_html(url)
    return parse_html(html)
