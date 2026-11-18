from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def hola():
    # el hostname de un contenedor en Kubernetes es el nombre del pod
    return f"Hola v5A desde el pod {socket.gethostname()}\n"

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    # 8082 y no 8080: el 8080 lo ocupa Jenkins
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8082")))
