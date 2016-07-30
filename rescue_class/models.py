# models.py

from flask_sqlalchemy import SQLAlchemy
from rescue_class import app



db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), primary_key=True, unique=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    gender = db.Column(db.String(30))
    picture = db.Column(db.String(120))
    access_token = db.Column(db.String(120), unique=True)


    def __init__(self, profile):
        self.email = profile.get('email', '')
        self.firstname = profile.get('given_name', '')
        self.lastname = profile.get('family_name', '')
        self.gender = profile.get('gender', '')
        self.picture = profile.get('picture', '')

    def __repr__(self):
        return self.email

    def is_active(self):
        return True

    def is_authenticated(self):
        """
        Returns `True`. User is always authenticated. Herp Derp.
        """
        return True

    def is_anonymous(self):
        """
        Returns `False`. There are no Anonymous here.
        """
        return False

    def get_id(self):
        """
        Assuming that the user object has an `id` attribute, this will take
        that and convert it to `unicode`.
        """
        try:
            return unicode(self.email)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    def get_field(self, key):
        return getattr(self, key) # same: self.key

    def update_field(self, key, value):
        user = get_user(self.email)
        setattr(user, key, value)  # same: user.key = value
        db.session.commit()


###############################################################################
# helper function used by any other class that wants to add users
###############################################################################
def create_user(profile):
    email = profile.get('email')
    user = None

    if not User.query.filter_by(email=email).first():
        new_user = User(profile)
        db.session.add(new_user)
        db.session.commit()
        print 'added new user: %s' % email
    else:
        print '%s already exists.' % email

    user = User.query.filter_by(email=email).first()
    return user

def get_user(user_id):
    return User.query.filter_by(email=user_id).first()

def get_all_users():
    return User.query.all()
