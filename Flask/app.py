from flask import Flask, request, jsonify
import os
from supabase import create_client, Client
import importlib.metadata

app = Flask(__name__)
try:
    flask_version = importlib.metadata.version('Flask')
except importlib.metadata.PackageNotFoundError:
    flask_version = 'unknown'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

    
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.post('/signup')
def signup():
    data = request.get_json()
    email = data.get('email')   
    password = data.get('password')
    result = supabase.auth.sign_up({"email": email, "password": password})
    print(result)
    
    if result.user is None:
        return jsonify({"error": result}), 400

    return {'message': 'User signed up successfully'}    

@app.route('/health')
def health():
    return {'OK': 200, 'Flask Version': flask_version}

if __name__ == '__main__':
    app.run(debug=True)

