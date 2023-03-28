from app import app
import messages, users, projects
from flask import render_template, request, redirect

@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route("/add", methods=["get", "post"])
def add_project():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html"), message="Nimessä tulee olla 1-20 merkkiä")
        
        material = request.form["material"]
        if len(material) < 1 or len(material) > 20:
            return render_template("error.html"), message="Vastauksessa tulee olla 1-20 merkkiä")

        start_date = request.form["start_date"]
        finishing_date = request.form["finishing_date"]

        project_id = projects.add_project(users.user_id(), name, material, start_date, finishing_date)
        return redirect("/projects/+str(project_id))

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
