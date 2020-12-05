from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from flask_mysqldb import MySQL
from helpers import login_required

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Config MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'book_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init Mysql
mysql = MySQL(app)

posts = [
    {
        'textbook_id': 1,
        'description': 'First book in the store',
        'edition': 2,
        'isbn': '9877 456 758',
        'name': 'Harry Potter',
        'price': 28,
        'book_volume': 1
    },
    {
        'textbook_id': 2,
        'description': 'last edition',
        'edition': 3,
        'isbn': '9554 858 101',
        'name': 'Arch de Triomph',
        'price': 8,
        'book_volume': 2
    }
]


@app.route('/textbook/<string:id>/')
def textbook(id):
    """Return list of all books available"""
    return render_template('textbook.html', id=id)


@app.route('/')
@app.route('/home')
# @login_required
def index():
    """
    home page of the web application
    :return: nothing
    """
    return render_template('index.html')


@app.route('/shop')
@login_required
def shopping():
    """ Shopping page of the web app"""
    return render_template('shop.html', posts=posts)


@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    """About page of the web app"""
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide student number")
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        username = request.form.get('username')
        password = request.form.get('password')

        # Create cursor
        db = mysql.connection.cursor()

        # Query database for user
        rows = db.execute("SELECT * FROM student WHERE std_number=%s", [username])
        print(type(rows))

        # Ensure username exists and password is correct
        if rows > 0:
            data = db.fetchall()
            if len(data) != 1:
                return render_template("error.html", message='invalid username and/or password')

            session["user_id"] = data
            return redirect("/")

        else:
            print('not user')
            return render_template('error.html', message='not user found')

        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        # return redirect("/")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure firstname was submitted
        if not request.form.get("firstname"):
            return render_template("error.html", message="Missing firstname")
        elif not request.form.get("lastname"):
            return render_template("error.html", message="Missing lastname")
        elif not request.form.get("student_number"):
            return render_template("error.html", message="Missing student number")
        elif not request.form.get("email"):
            return render_template("error.html", message="Missing email")
        elif not request.form.get("password"):
            return render_template("error.html", message="Must provide password")
        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")

        # linking model (html) to the controller (Python code)
        firstname = request.form.get("firstname")
        middle_name = request.form.get("middle_name")
        lastname = request.form.get("lastname")
        student_number = request.form.get("student_number")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # checking password validation
        if password != confirmation:
            return render_template("error.html", message="password did not match")

        # hashing password for security reason
        password_hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Create cursor
        db = mysql.connection.cursor()

        # Query database for user
        rows = db.execute("SELECT * FROM student WHERE std_number=%s", [student_number])
        mysql.connection.commit()

        if rows != 0:
            return render_template("error.html", message="user already exist")

        db.execute("INSERT INTO student(first_name, middle_name, last_name, std_number, email_address, password) VALUES(%s, %s, %s, %s, %s, %s)", (firstname, middle_name, lastname, student_number, email, password_hashed))

        # Commit to database
        mysql.connection.commit()

        # Close connection
        db.close()

        flash('User successfully created')
        # Redirect user to login page
        return redirect(url_for("login"))

    else:
        return render_template("register.html")


@app.route('/team')
@login_required
def team():
    """
    This is team html page
    :return: html page
    """
    return render_template('team.html')


@app.route('/account')
def account():
    """ Account profile"""
    return render_template('account.html')


@app.route('/logout')
def logout():
    """Log user out"""

    # Clear any user_id
    session.clear()

    # Redirect to home page
    return redirect('/')


if __name__ == '__main__':
    app.run()
