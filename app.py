from flask import Flask, render_template, request

from helpers import login_required

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    if request.method == "GET":
        return render_template('index.html', name=request.args.get("name", "world"))
    if request.method == "POST":
        return render_template('greet.html', name=request.form.get("name", "world"))


@app.route('/about', methods=['GET', 'POST'])
def about():
    """About page of the web app"""
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        if not name:
            return render_template("error.html", message="Missing name")
        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="Missing password")
        password_confirmation = request.form.get("confirmation")
        if not password_confirmation:
            return render_template("error.html", message="Missing password confirmation")
        if password_confirmation != password:
            return render_template("error.html", message="Password does not match")

    else:
        return render_template("register.html")


@app.route('/registrant')
def reg():
    """i will be back on this method"""
    return "TODO"


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
