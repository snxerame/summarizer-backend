from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/fetch-html", methods=["POST"])
def fetch_html():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not url.startswith("http"):
        return jsonify(error="Invalid URL"), 400
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500
    return jsonify(html=html)
