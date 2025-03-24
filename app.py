from flask import Flask, render_template, jsonify, request, session, redirect, url_for,flash
from database import get_job_list, get_job_data, add_user,get_user,delete_job_data,add_job_data
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
    job_list = get_job_list()  
    return render_template('home.html', jobs=job_list)

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
    user_data = get_user(username)
    password_hash = user_data['password_hash']
    if password_hash:
        flag = bcrypt.check_password_hash(password_hash,password)
        if flag:
            session["username"] = username
            session["user_type"] = user_data['user_type']
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

@app.route('/delete-job/<id>')
def delete_job(id):
    delete_job_data(id)
    return redirect(url_for('home'))


@app.route('/post-job')
def post_job():
    if session['user_type'] == 'recruiter':
        return render_template('postjob.html')

@app.route('/add-job',methods = ['POST'])
def add_job():
    if session['user_type'] == 'recruiter':
        data = request.form
        posted_by = session['username']
        title = data.get('title')
        salary = data.get('salary')
        salary = int(salary) if salary.isdigit() else None
        company = data.get('company')
        location = data.get('location')
        responsibilities = data.get('responsibilities')
        requirements = data.get('requirements')
        flag = add_job_data(title,salary,company,location,responsibilities,requirements,posted_by)
        if flag:
            flash("You have successfully uploaded a job post", "success")
            return redirect((url_for('home')))
        
        else : 
            flash("There has been an invalid input. TRY AGAIN!!", "danger")
            return redirect((url_for('post_job')))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

