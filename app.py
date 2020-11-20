from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        return render_template('greet.html', name=request.form.get("name", "world"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
