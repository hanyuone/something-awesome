import json
import os
import redis

from flask import Flask, request, send_from_directory, render_template, jsonify

app = Flask(__name__, template_folder="client/public")
db = redis.from_url(os.environ["REDISCLOUD_URL"])
db.set("files", "[]")

# Backend routes (API)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()

    files = json.loads(db.get("files"))
    files.append({
        "name": data["name"],
        "pages": data["pages"],
        "time": data["time"]
    })
    db.set("files", json.dumps(files))

    return jsonify({}), 200

# Svelte routes

@app.route("/")
def base():
    rendered = render_template("index.html", files=db.get("files").decode("utf-8"))
    return rendered

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

if __name__ == "__main__":
    app.run(port=3000)
