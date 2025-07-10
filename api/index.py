from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def get_html_with_curl(url):
    try:
        result = subprocess.run(
            ['curl', url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return None, str(e)

@app.route("/fetch-html", methods=["POST"])
def fetch_html():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not url.startswith("http"):
        return jsonify(error="Invalid URL"), 400
    html, error = get_html_with_curl(url), None
    if isinstance(html, tuple):
        html, error = html
    if html is None:
        return jsonify(error=error or "Failed to fetch HTML"), 500
    return jsonify(html=html)
