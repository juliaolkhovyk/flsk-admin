from app import app, db
from app.models import User, Group, Applicant

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Group': Group, 'Applicant': Applicant}