from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

CAPITALIQ_PREFIX = "https://www.capitaliq.spglobal.com/Articles/"

def fetch_capitaliq_images(page_url: str) -> list[str]:
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
    except requests.RequestException as e:
        print(f"Request failed: {e}")
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
        # Only add if src is an absolute Capital IQ image URL
        if src and src.startswith(CAPITALIQ_PREFIX):
            links.add(src)
    return sorted(links)

@app.route("/fetch-images", methods=["POST"])
def fetch_images():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not url.startswith("http"):
        return jsonify(error="Invalid URL"), 400
    return jsonify(images=fetch_capitaliq_images(url))
