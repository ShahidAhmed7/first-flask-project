from flask import Flask,render_template,jsonify
from database import get_job_list, get_job_data

app = Flask(__name__)

job_list = get_job_list()

@app.route('/')
def home():
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
    data = get_job_data(id)
    if data is None:
        return "Not found", 404  # Handle missing job data
    return render_template("jobpage.html",job = data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

