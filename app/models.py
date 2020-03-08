from datetime import datetime
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mail = db.Column(db.String(64), unique=True)
    password = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def is_mail_valid(self):
        return validate_email(self.mail)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def password_valid(self, password):
        return check_password_hash(self.password, password)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    status = db.Column(db.Enum('набирается', 'набрана', 'идет', 'в архиве',
                                name='status_type'), default='идет')
    course = db.Column(db.Enum('python', 'vue', 'django', 'php', 'html',
                                name='course_type'), default='python')
    start = db.Column(db.DateTime, default=datetime.today())
    applicants = db.relationship('Applicant', back_populates='group')
    seats = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.title)

    @property
    def count_seats(self):
        return len(self.applicants)


class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    mail = db.Column(db.String(64), unique=True)
    status = db.Column(db.Enum('новая', 'обрабатывается', 'оплачена', 
                    'распределена в группу', name='status_applicant_type'),
                    default='новая')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Group', back_populates='applicants')
    
    def is_mail_valid(self):
        return validate_email(self.mail)
    
    def __repr__(self):
        return '{}'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))




