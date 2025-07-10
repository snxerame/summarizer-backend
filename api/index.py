from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

PREFIX = ""

def is_valid(url: str) -> bool:
    p = urlparse(url)
    return p.scheme and p.netloc

def fetch_image_links(page_url: str) -> list[str]:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(page_url, headers=headers, timeout=8)
        resp.raise_for_status()
    except requests.RequestException:
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    links = set()
    for img in soup.find_all("img"):
        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-original")
            or img.get("data-lazy")
        )
        if src:
            abs_url = urljoin(page_url, src)
            if is_valid(abs_url) and abs_url.startswith(PREFIX):
                links.add(abs_url)
    return sorted(links)

@app.route("/fetch-images", methods=["POST"])
def fetch_images():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not is_valid(url):
        return jsonify(error="Invalid URL"), 400
    return jsonify(images=fetch_image_links(url))
