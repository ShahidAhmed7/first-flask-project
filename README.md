# BRAC Careers Job Portal

**BRAC Careers** is a job portal specifically designed for **BRAC University students**. It allows students to view job listings, apply directly via email, and manage their applications. Recruiters can post and manage job listings on the platform.

---

## Features

- **Applicants** can:
  - View available job listings.
  - Apply directly via email to the recruiter.
  
- **Recruiters** can:
  - Post new job listings.
  - Update and manage existing job postings.

- **User Authentication**: Two user roles — **Recruiter** and **Applicant**. Applicants can only view and apply for jobs. Recruiters can post and manage jobs.

- **Email Integration**: Applicants can apply via email by opening Gmail with pre-filled application details.

---

## Technologies Used

- **Flask**: Web framework for handling backend functionality.
- **MySQL**: Database to store job listings, user credentials, and applications.
- **Bootstrap**: Front-end framework for responsive design.
- **bcrypt**: Password hashing for secure authentication.
- **Jinja2**: Templating engine for dynamic HTML rendering.

---

## What I Have Learned

- **Flask Web Framework**: Learned to use Flask for backend development, handling routing, and building dynamic web applications.
- **HTML/CSS**: Gained experience in building responsive front-end layouts using HTML and CSS, utilizing Bootstrap for clean design.
- **SQL and MySQL**: Learned to set up and interact with MySQL databases using SQLAlchemy in Flask, managing user authentication and job data.
- **User Authentication**: Implemented user authentication with password hashing (bcrypt) and role-based access control (Recruiter and Applicant).
- **Jinja2 Templating**: Used Jinja2 to create dynamic HTML templates that render data from Flask routes.
- **Email Integration**: Integrated a feature where applicants can apply directly via email, pre-filled with job details.
- **Flashing Messages**: Implemented Flash messages for user feedback (e.g., login success or error).

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/brac-careers.git
   cd brac-careers

2. Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up MySQL and update config.py with the database details.

5. Run the app:
```bash
flask run
```
6. Access the portal at http://127.0.0.1:5000.

