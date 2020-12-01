from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from flask_mysqldb import MySQL
from helpers import login_required

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'textbook'
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
def shopping():
    """ Shopping page of the web app"""
    return render_template('shop.html', posts=posts)


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
        lastname = request.form.get("lastname")
        student_number = request.form.get("student_number")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Create cursor
        db = mysql.connection.cursor()

        # Query database for user
        #rows = db.execute("SELECT * FROM student WHERE email= :email",
        #                  email=request.form.get("email"))

        #if len(rows) != 0:
         #   return render_template("error.html", message="user already exist")
        db.execute("INSERT INTO student(first_name, last_name, stud_number, email) VALUES(%s, %s, %s, %s)", (firstname, lastname, student_number, email))

        # Commit to database
        mysql.connection.commit()

        # Close connection
        db.close()
        flash('Success')

        return redirect("login.html")

    else:
        return render_template("register.html")


@app.route('/team')
def team():
    """
    This is team html page
    :return: html page
    """
    return render_template('team.html')


if __name__ == '__main__':
    app.run()
