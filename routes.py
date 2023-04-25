from app import app
import reviews, messages, users, projects, instructions
from flask import render_template, request, redirect

@app.route("/")
def index():
    list = messages.get_list()
    p_list = projects.get_projects()
    o_list = instructions.get_instructions()
    return render_template("index.html", count=len(list), messages=list, p_count=len(p_list), projects=p_list, o_count=len(o_list), instructions=o_list)

@app.route("/own_projects", methods=["get"])
def own_projects():

    if request.method == "GET":
        list = projects.get_my_projects(users.user_id())
        return render_template("own_projects.html", count=len(list), projects=list)

@app.route("/add", methods=["get", "post"])
def add_project():
    if request.method == "GET":
     instruction_list = instructions.get_instructions()   
     return render_template("add.html", instruction_list=instruction_list)

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimessä tulee olla 1-20 merkkiä")
        
        material = request.form["material"]
        if len(material) < 1 or len(material) > 50:
            return render_template("error.html", message="Materiaalin vastauksessa tulee olla 1-50 merkkiä")

        start_date = request.form["start_date"]

        finishing_date = request.form["finishing_date"]
        
        instruction_used = request.form["instruction_used"]
        
        project_id = projects.add_project(users.user_id(), name, material, start_date, finishing_date, instruction_used)
        return redirect("/projects/"+str(project_id))

@app.route("/add_instruction", methods=["get", "post"])
def add_instruction():
    if request.method == "GET":
        return render_template("add_instruction.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimessä tulee olla 1-20 merkkiä")

        content = request.form["content"]
        if len(content) < 1 or len(content) > 10000:
            return render_template("error.html", message="Ohjeessa tulee olla 1-10000 merkkiä")

        difficulty = request.form["difficulty"]

        instruction_id = instructions.add_instruction(users.user_id(), name, content, difficulty)
        return redirect("/instructions/"+str(instruction_id))

@app.route("/remove", methods=["get", "post"])
def remove_project():

    if request.method == "GET":
        my_projects = projects.get_my_projects(users.user_id())
        
        if len(my_projects) < 1:
            return render_template("error.html", message="Sinulla ei vielä ole projekteja")

        return render_template("remove.html", list=my_projects)
    
    if request.method == "POST":
        users.check_csrf()

        if "project" in request.form:
            project = request.form["project"]
            projects.remove_project(project, users.user_id())

        return redirect("/")

@app.route("/remove_instruction", methods=["get", "post"])
def remove_instruction():

    if request.method == "GET":
        my_instructions = instructions.get_my_instructions(users.user_id())

        if len(my_instructions) < 1:
            return render_template("error.html", message="Sinulla ei vielä ole ohjeita")

        return render_template("remove_instruction.html", list=my_instructions)

    if request.method == "POST":
        users.check_csrf()

        if "instruction" in request.form:
            instruction = request.form["instruction"]
            instructions.remove_instruction(instruction, users.user_id())

        return redirect("/")

@app.route("/remove_message", methods=["get", "post"])
def remove_message():

    if request.method == "GET":
        my_messages = messages.get_my_messages(users.user_id())

        if len(my_messages) < 1:
            return render_template("error.html", message="Et ole lähettänyt yhtään viestiä")

        return render_template("remove_message.html", list=my_messages)

    if request.method == "POST":
        users.check_csrf()

        if "message" in request.form:
            message = request.form["message"]
            messages.remove_message(message, users.user_id())

        return redirect("/")

@app.route("/remove_review", methods=["get", "post"])
def remove_review():

    if request.method == "GET":
        my_reviews = reviews.get_my_reviews(users.user_id())

        if len(my_reviews) < 1:
            return render_template("error.html", message="Et ole arvioinut mitään")

        return render_template("remove_review.html", list=my_reviews)

    if request.method == "POST":
        users.check_csrf()

        if "review" in request.form:
            review = request.form["review"]
            reviews.remove_review(review, users.user_id())

        return redirect("/")

@app.route("/projects/<int:project_id>")
def show_project(project_id):
    info = projects.get_project_info(project_id)
    i_info = projects.get_project_instruction(project_id)    
    reviews = projects.get_review(project_id)    

    return render_template("projects.html", id=project_id, name=info[0], material=info[1],
                           start_date=info[2], finishing_date=info[3], creator=info[4], reviews=reviews, i_info=i_info)

@app.route("/instructions/<int:instruction_id>")
def show_instruction(instruction_id):
    info = instructions.get_instruction_info(instruction_id)
    
    reviews = instructions.get_review(instruction_id)    

    return render_template("instructions.html", id=instruction_id, name=info[0], content=info[1],
                           difficulty=info[2], creator=info[3], reviews=reviews)

@app.route("/review", methods=["post"])
def review():
    users.check_csrf()

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

@app.route("/review_instruction", methods=["post"])
def review_instruction():
    users.check_csrf()

    instruction_id = request.form["instruction_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Virheellinen tähtimäärä")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if comment == "":
        comment = "-"

    instructions.add_review(instruction_id, users.user_id(), stars, comment)

    return redirect("/instructions/"+str(instruction_id))

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if len(content) > 1000:
        return render_template("error.html", message="Viesti on liian pitkä")
    if content == "":
        return render_template("error.html", message="Viesti on liian lyhyt")
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
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")        

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Tyhjä salasana ei kelpaa")
        if len(password1) < 8:
            return render_template("error.html", message="Salasanan tulee olla vähintään 8 merkkiä pitkä")

        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
