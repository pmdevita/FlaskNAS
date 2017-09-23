print("importing flask")
from flask import Flask, send_from_directory, redirect, url_for, request, session, render_template, jsonify, \
    make_response
from flask_session import Session
print("flask imported")
from core import constants as consts
from core import database
from core.files import Files, InvalidPath
from core.config import Config
import os, json


resourcespath = os.path.abspath("core/resources")
app = Flask(__name__, template_folder=os.path.join(resourcespath, "templates"))
app.config["SECRET_KEY"] = consts.secretkey()

def _redis_check(v):
    # Is Redis available?
    app.config["SESSION_TYPE"] = "filesystem"
    if "redis" in config.keys():
        v.update(["redis"])
        try:
            import redis
            app.config["SESSION_TYPE"] = "redis"
        except ImportError:
            pass

        # Try to load Redis config
        if app.config["SESSION_TYPE"] == "redis":
            print("Enabling Redis")
            manual = False
            if "host" in config['redis'].keys() or "port" in config['redis'].keys():
                manual = True
            app.config["SESSION_REDIS"] = redis.StrictRedis(host=config["redis"].get('host', "localhost"),
                                                            port=config["redis"].get('port', 6379))


users = database.Users()
shares = database.Shares()

class WebConsts:
    name = "Peter's NAS Manager"

# First time login activated by choosing login template, which triggers correct API endpoints
# to finish setup
login_page = "login.html"
if users.no_users:
    login_page = "first_login.html"
    import platform
    WebConsts.hostname = platform.uname()[1]

# We cannot initialize files with path because path may not be available right now
config = Config()
files = Files(config)


@app.route("/")
def root():
    if "username" in session:
        return render_template("index.html", v=WebConsts, user=session["username"])
    else:
        global login_page
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
    if "username" in session:   # If we are logged in, normal operations are available
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
    else:                       # Otherwise, only the login api is available
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
    

# Resources (not necessary in production since it will be provided by NGINX)
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

def start(venv, debug=False):
    print("starting flask")
    _redis_check(venv)
    Session(app)
    if debug:
        app.debug = True
        app.run(host="0.0.0.0")
    else:
        return app