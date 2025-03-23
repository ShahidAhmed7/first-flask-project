from flask import Flask, render_template, jsonify, request, session, redirect, url_for,flash, get_flashed_messages
from database import get_job_list, get_job_data, add_user,get_user
from flask_session import Session
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config["SESSION_PERMANENT"] = False #ensures the session is not persistent across browser sessions.
app.config["SESSION_TYPE"] = "filesystem" #stores the session on the server's filesystem.
Session(app)

job_list = get_job_list()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('check_login'))
    return render_template('home.html',jobs = job_list)

@app.route('/api/jobs')
def list_jobs():
    return jsonify(job_list)

@app.route('/api/jobs/<id>')
def show_job_data(id):
    data = get_job_data(id)
    return jsonify(data)

@app.route('/jobs/<id>')
def apply_job_data(id):
    if 'username' not in session:
        return redirect(url_for('check_login'))
    data = get_job_data(id)
    if data is None:
        return "Not found", 404  # Handle missing job data
    return render_template("jobpage.html",job = data)

@app.route('/register', methods = (['POST','GET']))
def check_registration():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.form
    user_type = data.get('user_type')
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    flag = add_user(user_type, name, username, email, password_hash)
    
    if flag:
        flash("You have successfully signed up", "success")  # Green Success Message
        return redirect(url_for('check_login'))
    else:
        
        flash("Same username or email already exists. Try a different one", "danger")  # Red Error Message
        return redirect(url_for('check_registration'))

    
@app.route('/login', methods = (['GET','POST']))
def check_login():
    if request.method == 'GET':
        return render_template('loginpage.html')

    data = request.form
    password = data.get('password')
    username = data.get('username')
    password_hash = get_user(username)
    if password_hash:
        flag = bcrypt.check_password_hash(password_hash,password)
        if flag:
            session["username"] = username
            return redirect((url_for('home')))
        else:
            flash("Invalid username or password", 'danger')
            return render_template('loginpage.html')
        
    else:
        flash("Username doesn't exist. Please sign up.", 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def do_logout():
    session.clear()
    return redirect(url_for('check_login'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

