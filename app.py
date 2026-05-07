from flask import Flask
import socket
app = Flask(__name__)

@app.route("/")
def hello():
    return f"Hello from CI/CD! v2 — served by pod {socket.gethostname()}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
