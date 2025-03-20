from flask import Flask,render_template,jsonify
from database import get_job_list

app = Flask(__name__)

job_list = get_job_list()

@app.route('/')
def home():
    return render_template('home.html',jobs = job_list)

@app.route('/api/jobs')
def list_jobs():
    return jsonify(job_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

