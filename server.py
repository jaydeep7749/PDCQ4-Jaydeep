from flask import Flask, url_for, session, redirect, render_template, request
from authlib.integrations.flask_client import OAuth
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.secret_key = "3390a726-9a16-410f-8318-972c1cc6ed4f"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id="363059848334-26rd2jt9k5av8p8gn0jq5vkfenhbe7md.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile"
    }
)

def get_current_indian_time():
    india_tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")


def design_pattern(num_lines):
    base = "FORMULAQSOLUTIONS"
    result = []
    width = num_lines * 2  

    
    config = [
        (0, 0),        
        (1, 1),        
        (2, 0),       
        (3, 5),        
        (4, 0),        
        (5, 11),       
        (6, 0),       
        (7, 16),       
        (8, 0),       
        (9, 16),       
        (10, 0),      
        (11, 11),      
        (12, 0),       
        (13, 5),      
        (14, 0),       
        (15, 1),       
        (16, 0),      
    ]
    
    pattern_map = [
        ("F", ""),
        ("O", "M"),
        ("RMULA", ""),
        ("M", "O"),
        ("ULAQSOLUT", ""),
        ("L", "N"),
        ("AQSOLUTIONSFO", ""),
        ("Q", "U"),
        ("SOLUTIONSFORMULAQ", ""),
        ("O", "A"),
        ("LUTIONSFORMUL", ""),
        ("U", "U"),
        ("TIONSFORM", ""),
        ("I", "R"),
        ("ONSFO", ""),
        ("N", "F"),
        ("S", ""),
    ]
    dash_counts = [0, 1, 0, 5, 0, 11, 0, 16, 0, 16, 0, 11, 0, 5, 0, 1, 0]
    for i in range(num_lines):
        left, right = pattern_map[i]
        dashes = "-" * dash_counts[i]
        line = left + dashes + right
        result.append(line)
    return result


for line in design_pattern(17):
    print(line)



@app.route("/", methods=["GET", "POST"])
def home():
    user = session.get('user')
    indian_time = get_current_indian_time()
    output = None
    error = None

    
    if user and request.method == "POST":
        num_lines_raw = request.form.get("num_lines", "").strip()
        if not num_lines_raw.isdigit():
            error = "Please enter a valid positive integer."
        else:
            num_lines = int(num_lines_raw)
            if not (1 <= num_lines <= 100):
                error = "Please enter a number between 1 and 100."
            else:
                output = design_pattern(num_lines)
    return render_template("home.html", user=user, indian_time=indian_time, output=output, error=error)

@app.route("/google-login")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, prompt='select_account')

@app.route("/signin-google")
def google_callback():
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    session["user"] = {
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
        "picture": userinfo.get("picture")
    }
    return redirect(url_for("home"))

@app.route("/signout")
def signout():
    session.pop('user', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

