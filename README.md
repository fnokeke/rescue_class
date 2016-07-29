# Intro
Rescue Class is a research project that uses RescueTime for students in class. The goal is to
 provide personalized feedback to students and de-identified aggregated reports to instructors.

# Tools
- Flask
- Postgres
- HTML, CSS, Javascript

# How to
- activate virtualenv and install libraries: `pip install -r requirement.txt`
- start server: `python runserver.py`
- Go to your server link: http://localhost:5590 # or your set port

# Database Setup
- Start redis server: redis-server
- Start postgresql server by launching Postgres application
- Create postgres database: `create database rescuedb with owner postgres;`
- In iPython, create all tables from your models: `db.create_all()` # you can do this by importing SQLAlchemy db object from your models module.
- Commit changes: db.session.commit(). You can also use Postico OSX app as a gui for your DB.
