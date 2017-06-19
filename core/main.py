print("importing flask")
from flask import Flask, send_from_directory, redirect, url_for, request, session, render_template, jsonify, make_response
print("flask imported")
from core import constants as consts
from core import database
from core.files import Files, InvalidPath
from core.config import Config
import os, json


resourcespath = os.path.abspath("core/resources")
app = Flask(__name__, template_folder=os.path.join(resourcespath, "templates"))
app.secret_key = consts.secretkey()

users = database.Users()
shares = database.Shares()

class WebConsts:
    name = "Peter's NAS Manager"

# First time login activated by choosing login template, which triggers correct API endpoints
# to finish setup
global login_page
login_page = "login.html"
if users.no_users:
    login_page = "first_login.html"
    import platform
    WebConsts.hostname = platform.uname()[1]

# We cannot initalize files with path because path may not be available right now
config = Config()
files = Files(config)



@app.route("/")
def root():
    if "username" in session:
        return render_template("index.html", v=WebConsts, user=session["username"])
    else:
        return render_template(login_page, v=WebConsts)
        # return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))

@app.route("/api",  methods=["POST"])
@app.route("/api/<path:path>",  methods=["POST"])
def api(path=None):
    # path = path.split()
    if "username" in session:
        # File Access
        if request.form.get("point", None) == "files":
            if request.form.get("what", None) == "shares":
                print(files.list_shares())
                return jsonify(files.list_shares())

            if request.form.get("what", None) == "listing":
                try:
                    dir_list = files.get_listing(request.form["path"])
                except InvalidPath:
                    return "", 400
                return jsonify(dir_list)

        # Logout
        elif request.form.get("point", None) == "logout":
                session.pop('username', None)
                return redirect(url_for('root'))
    else:
        # Login
        global login_page
        if request.form.get("point", None) == "login" and "username" in request.form and "password" in request.form:
            if users.login(request.form["username"], request.form["password"]):
                if "remember" in request.form:
                    session.permanent = True
                session["username"] = request.form["username"]
                return jsonify({"Response": "Success", "Action": "Redirect"})
            else:
                return jsonify({"Response": "Error", "Error": "Username/Password incorrect"})
        # First Login
        elif request.form.get("point", None) == "first_login" and login_page == "first_login.html":
            if request.form.get("username", None) and request.form.get("password") and \
                request.form.get("NASname", None) and request.form.get("group", None) and \
                request.form.get("path", None):
                    users.create_first_user(request.form["username"], request.form["password"])
                    config["rootpath"] = request.form["path"]
                    shares.global_config["netbios name"] = request.form["NASname"]
                    shares.global_config["group"] = request.form["group"]

                    login_page = "login.html"
                    session["username"] = request.form["username"]
                    return jsonify({"Response": "Success", "Action": "Redirect"})

    return 400
    

# Resources (probably not necessary in production)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    r = make_response(send_from_directory("resources/static", path))
    # stop caching chrome omg
    if app.debug:
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def debugrun(debug=False):
    print("starting flask")
    if debug:
        app.debug = True
    app.run(host="0.0.0.0")