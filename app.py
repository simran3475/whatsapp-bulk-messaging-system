from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

import cli_functions as cli

import os

# users_and_tables = {} # {"username": [table1, table2, table3]}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a table containing the list of users(string) their name(string) login_password(string) and the tables(json) they have creted
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    login_password = db.Column(db.String(50), nullable=False)
    tables = db.Column(db.JSON(50), default={})

    def __repr__(self):
        # return {'username': self.username, 'login_password': self.login_password, 'tables': self.tables}
        return f"(username:{self.username}, name:{self.name}, password:{self.login_password}, tables:{self.tables})"

with app.app_context():
    db.create_all()

# admin = User(username='admin', name = "tashif", login_password='000', tables={0:"f", 1:"g", 2:"h"})
# with app.app_context():
#     db.session.add(admin)
#     db.session.commit()

def all_details():
    with app.app_context():
        all_users = User.query.all()
        ids = [user.id for user in all_users]
        users = [user.username for user in all_users]
        names = [user.name for user in all_users]
        passwords = [user.login_password for user in all_users]
        tables = [user.tables for user in all_users]
        return ids, users, names, passwords, tables

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        login_password = request.form['pass']
        data = all_details()
        if username in data[1] and login_password == data[3][data[1].index(username)]:
            return render_template("buttons.html", username=username, tables=data[-1][data[1].index(username)], name=data[2][data[1].index(username)].title())
        else:
            return render_template('index.html', error_message='Invalid username or password')
    else:
        return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['c_name']
        username = request.form['c_email']
        login_password = request.form['c_pass']
        data = all_details()
        if username in data[1]:
            error_message = 'Email already exists. Please use a different email.'
            return render_template('index.html', error_message=error_message)
        else:
            user = User(username=username, name=name, login_password=login_password, tables={})
            with app.app_context():
                db.session.add(user)
                db.session.commit()
            return render_template('index.html', success_message='Account created successfully. Please login to continue.')
    else:
        return render_template('signup.html')

@app.route('/tables')

def load(link ,username):
    return render_template(link, username=username)
# @app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload(username):
    # render_template('after_login.html', username=username)
    load('after_login.html', username)
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if request.method == 'POST':
        # check if the postgit  request has the file part
        if 'file' not in request.files:
            return render_template('after_login.html', error='No file part')

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('after_login.html', error='No selected file')

        if allowed_file(file.filename) == False:
            return render_template('after_login.html', error='File type not supported. You can only upload csv, xlsx and xls files')
        else: 
            # Save the file to the desired location
            filename = f"{username}_{secure_filename(file.filename)}"
            details = all_details()
            user = User.query.filter_by(username=username).first()
            len_json = len(user.tables)
            user.tables[len_json] = filename
            file.save(os.path.join('uploads/', filename))
            db.session.commit()

        return render_template('buttons.html', success='File successfully uploaded')

    return render_template('after_login.html')

@app.route("/tables/<username>", methods=['GET', 'POST'])
def load_tables(username):
    data = all_details()
    tables = data[-1][data[1].index(username)]
    length = len(tables)
    return render_template('tables.html', tables=tables, length=length, username=username)

@app.route("/tables/<username>")
# def show()

@app.route('/<username>/<table_name>', methods=['GET'])
def create_table(username, table_name):
    data = all_details()
    # Check if the username exists in the database
    if username not in data[1]:
        return f"User {username} does not exist"
        return redirect('/signup')
    else:
        if table_name in data[3][data[1].index(username)]:
            return f"Table {table_name} already exists for user {username}"
            return redirect('/login')

    # Define a dynamic table class for each user and table combination
    table_class_name = f"{username}_{table_name}"
    DynamicTable = type(table_class_name, (db.Model,), {
        'id': db.Column(db.Integer, primary_key=True),
        'data': db.Column(db.String(50), nullable=False)
    })
    '''
    Dynamic Allocation of Database Tables explaained:
    - table_class_name: It's a string that combines username and table_name to create a unique identifier for the table class. This ensures that each user and table combination has a distinct table class name.
    - DynamicTable: This is the dynamically created table class. It uses the type() function to create a new class with the given name (table_class_name). The parameters for type() are:
    - table_class_name: The name of the new class.
    - (db.Model,): A tuple of base classes for the new class. In this case, it inherits from db.Model, which is the base class for SQLAlchemy models.
        The third argument is a dictionary that defines the attributes of the class. In this case:
        'id': db.Column(db.Integer, primary_key=True): It defines an id column of type Integer, which serves as the primary key for the table.
        'data': db.Column(db.String(50), nullable=False): It defines a data column of type String with a maximum length of 50 characters, and it cannot be nullable.
        By dynamically creating the table class, you can adapt your database schema on-the-fly based on the user and table information provided in the URL. Each combination of username and table_name will have its own unique table class and, consequently, its own database table.

    Create the table in the database
    '''
    return f'Table {table_name} created for user {username} with table class {table_class_name}'

if __name__ == '__main__':
    app.run(debug=True)