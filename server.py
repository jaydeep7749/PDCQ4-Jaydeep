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


def design_pattern(num_lines): # part 2 for the pattern printing
    chars = "FORMULAQSOLUTIONS"
    n = num_lines
    pattern = []
    max_width = n  

    for i in range(n):
        if i < n // 2:
            left_char = chars[i]
            right_char = chars[n - i - 1]
            dashes = n - 2 * i - 2
            if dashes > 0:
                line = left_char + "-" * dashes + right_char
            elif dashes == 0:
                line = left_char + right_char
            else:
                line = left_char
        elif i == n // 2:
            line = chars[:n]
        else:
            mirror_i = n - i - 1
            left_char = chars[mirror_i]
            right_char = chars[n - mirror_i - 1]
            dashes = n - 2 * mirror_i - 2
            if dashes > 0:
                line = left_char + "-" * dashes + right_char
            elif dashes == 0:
                line = left_char + right_char
            else:
                line = left_char
        
        pattern.append(line.center(max_width))
    return pattern



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
