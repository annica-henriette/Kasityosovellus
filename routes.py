from app import app
import messages, users, projects, instructions
from flask import render_template, request, redirect

@app.route("/")
def index():
    list = messages.get_list()
    p_list = projects.get_projects()
    o_list = instructions.get_instructions()
    return render_template("index.html", count=len(list), messages=list, p_count=len(p_list), projects=p_list, o_count=len(o_list), instructions=o_list)

@app.route("/add", methods=["get", "post"])
def add_project():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimessä tulee olla 1-20 merkkiä")
        
        material = request.form["material"]
        if len(material) < 1 or len(material) > 20:
            return render_template("error.html", message="Vastauksessa tulee olla 1-20 merkkiä")

        start_date = request.form["start_date"]

        finishing_date = request.form["finishing_date"]

        project_id = projects.add_project(users.user_id(), name, material, start_date, finishing_date)
        return redirect("/projects/"+str(project_id))

@app.route("/add_instruction", methods=["get", "post"])
def add_instruction():
    if request.method == "GET":
        return render_template("add_instruction.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimessä tulee olla 1-20 merkkiä")

        content = request.form["content"]
        if len(content) < 1 or len(content) > 1000:
            return render_template("error.html", message="Vastauksessa tulee olla 1-1000 merkkiä")

        difficulty = request.form["difficulty"]

        instruction_id = instructions.add_instruction(users.user_id(), name, content, difficulty)
        return redirect("/instructions/"+str(instruction_id))

@app.route("/remove", methods=["get", "post"])
def remove_project():

    if request.method == "GET":
        my_projects = projects.get_my_projects(users.user_id())
        return render_template("remove.html", list=my_projects)

    if request.method == "POST":

        if "project" in request.form:
            project = request.form["project"]
            projects.remove_project(project, users.user_id())

        return redirect("/")

@app.route("/remove_instruction", methods=["get", "post"])
def remove_instruction():

    if request.method == "GET":
        my_instructions = instructions.get_my_instructions(users.user_id())
        return render_template("remove_instruction.html", list=my_instructions)

    if request.method == "POST":

        if "instruction" in request.form:
            instruction = request.form["instruction"]
            instructions.remove_instruction(instruction, users.user_id())

        return redirect("/")

@app.route("/projects/<int:project_id>")
def show_project(project_id):
    info = projects.get_project_info(project_id)
    
    reviews = projects.get_review(project_id)    

    return render_template("projects.html", id=project_id, name=info[0], material=info[1],
                           start_date=info[2], finishing_date=info[3], creator=info[4], reviews=reviews)

@app.route("/instructions/<int:instruction_id>")
def show_instruction(instruction_id):
    info = instructions.get_instruction_info(instruction_id)
    
    reviews = instructions.get_review(instruction_id)    

    return render_template("instructions.html", id=instruction_id, name=info[0], content=info[1],
                           difficulty=info[2], creator=info[3], reviews=reviews)

@app.route("/review", methods=["post"])
def review():
    project_id = request.form["project_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if comment == "":
        comment = "-"

    projects.add_review(project_id, users.user_id(), stars, comment)

    return redirect("/projects/"+str(project_id))

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
