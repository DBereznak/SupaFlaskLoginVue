from flask import Flask, request, redirect, url_for, jsonify, render_template
import os
import jwt
from functools import wraps
import requests
from supabase import create_client, Client
import importlib.metadata

app = Flask(__name__)
try:
    flask_version = importlib.metadata.version('Flask')
except importlib.metadata.PackageNotFoundError:
    flask_version = 'unknown'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
JWKS_URL= "https://wldqojurxwlchifgzjxm.supabase.co/auth/v1/jwks"
supabase: Client = create_client(url, key)

jwks = requests.get(JWKS_URL).json()


def verify_jwt(token: str):
    try:
        return jwt.decode(
            token, jwks, algorithms=["RS256"], audience="authenticated"
        )
    except Exception:
        return None
    
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        print("COOKIE TOKEN:", token)

        if not token:
            print("NO TOKEN FOUND")
            return redirect("/")

        # TEMP: trust presence of token for now
        return f(*args, **kwargs)

    return wrapper


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

@app.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')   
    password = data.get('password')
    try: 
        result = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password        
            }
        )
        response = jsonify({"success": True})
        response.set_cookie(
            "access_token",
            result.session.access_token,
            httponly=True,
            secure=False,  # True in production
            samesite="LAX"
        )
        return response

    except Exception as e:   
        return jsonify({
            "error": "Invalid login credentials"
        }), 400

@app.post("/signout")
def signout():
    supabase.auth.sign_out()
    response = jsonify({"success": True})
    response.set_cookie(
        "access_token",
        "",
        expires=0,
        httponly=True,
        secure=False,   # True in production
        samesite="Lax"
    )
    return response

@app.route('/verify')
def verified():
    return render_template('verify.html')

@app.get('/logintest')
@require_auth
def loggedin():
    return render_template('logintest.html')    

@app.route('/health')
def health():
    return {'OK': 200, 'Flask Version': flask_version}

if __name__ == '__main__':
    app.run(debug=True)

