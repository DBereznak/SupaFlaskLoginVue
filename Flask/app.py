from flask import Flask, render_template
import importlib.metadata

app = Flask(__name__)
try:
    flask_version = importlib.metadata.version('Flask')
except importlib.metadata.PackageNotFoundError:
    flask_version = 'unknown'
    
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/health')
def health():
    return {'OK': 200, 'Flask Version': flask_version}

