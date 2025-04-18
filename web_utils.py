import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def fetch_and_parse(url):
    html = fetch_html(url)
    return parse_html(html)
