print("importing flask")
from flask import Flask, send_from_directory, redirect, url_for, request, session, render_template, jsonify, make_response
print("flask imported")
from core import constants as consts
from core.files import Files, InvalidPath
from core.login import Login, UserAlreadyExists, IncorrectCredentials
import os, json


resourcespath = os.path.abspath("core/resources")
app = Flask(__name__, template_folder=os.path.join(resourcespath, "templates"))
app.secret_key = consts.secretkey()

l = Login()

with open(consts.SETTINGS) as f:
    settings = json.load(f)

files = Files(settings["rootdir"])

class webconsts:
    name = "Peter's NAS Manager"

@app.route("/")
def root():
    if "username" in session:
        return render_template("index.html", v=webconsts, user=session["username"])
    else:
        return render_template("login.html", v=webconsts)
        # return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", v=webconsts)
    elif request.method == "POST":
        try:
            l.get(request.form["username"], request.form["password"])
        except IncorrectCredentials:
            return jsonify({"Response": "Error", "Error": "Username/Password incorrect"})
        if "remember" in request.form:
            session.permanent = True

        session["username"] = request.form["username"]
        return jsonify({"Response": "Success", "Action": "Redirect"})

@app.route("/newlogin", methods=["GET", "POST"])
def newlogin():
    if request.method == "GET":
        return render_template("newlogin.html", v=webconsts)
    elif request.method == "POST":
        try:
            l.create(request.form["username"], request.form["password"])
        except UserAlreadyExists:
            return jsonify({"Response": "Error", "Error": "Username already exists"})
        session["username"] = request.form["username"]
        return jsonify({"Response": "Success", "Action": "Redirect"})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))

@app.route("/api",  methods=["POST"])
@app.route("/api/<path:path>",  methods=["POST"])
def api(path=None):
    # path = path.split()
    if "username" in session:
        if request.form["point"] == "files":
            if request.form["what"] == "shares":
                print(files.list_shares())
                return jsonify(files.list_shares())
            if request.form["what"] == "listing":
                try:
                    dirlist = files.get_listing(request.form["path"])
                except InvalidPath:
                    return "", 400
                return jsonify(dirlist)

    return 400
    




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    r = make_response(send_from_directory("resources/static", path))
    #stop caching chrome omg
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