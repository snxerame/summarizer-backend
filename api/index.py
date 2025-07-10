from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

PREFIX = "https://www.capitalig.spglobal.com/Articles/"

def is_valid(url: str) -> bool:
    p = urlparse(url)
    return p.scheme and p.netloc

def fetch_image_links(page_url: str) -> list[str]:
    try:
        resp = requests.get(page_url, timeout=8)
        resp.raise_for_status()
    except requests.RequestException:
        return []
    soup = BeautifulSoup(resp.text, "html.parser")
    links = {
        urljoin(page_url, tag.get("src", ""))
        for tag in soup.find_all("img")
    }
    return sorted(u for u in links if is_valid(u) and u.startswith(PREFIX))

@app.route("/fetch-images", methods=["POST"])
def fetch_images():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not is_valid(url):
        return jsonify(error="Invalid URL"), 400
    return jsonify(images=fetch_image_links(url))
