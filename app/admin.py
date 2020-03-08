from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_admin import AdminIndexView, expose
from app import app, db, login
from app.models import User, Group, Applicant
from app.forms import Authorization

class DashboardView(AdminIndexView):

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))
   
    @expose('/')
    @login_required
    def index(self):
        applicants = Applicant.query.all()
        ready_applicants = Applicant.query.filter_by(
            status = 'распределена в группу'
        ).all()
        groups = Group.query.all()
        return self.render('admin/admin_dashboard.html', 
                            applicants=applicants,
                            ready_applicants = ready_applicants,
                            groups=groups)

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        form=Authorization()
        if form.validate_on_submit():
            user = User.query.filter_by(mail=form.mail.data).first()
            if user is None or user.password != form.password.data:
                flash('wrong email or password')
                return redirect(url_for('admin.login'))
            if user.is_admin:
                login_user(user)
                return redirect(url_for('admin.index'))
            else:
                flash('you are not an admin')
                return redirect(url_for('admin.login'))
        return self.render("admin/auth.html", form=form)
    
    @expose('/logout/')
    def logout(self):
        logout_user()
        return redirect(url_for('admin.login'))


class MyUserView(ModelView, BaseModelView):
    column_labels = dict(name='Имя',
                        mail='Логин',
                        password='Пароль',
                        is_admin='Является ли администратором')



class MyGroupView(ModelView, BaseModelView):
    column_list=('title', 'start', 'course', 'seats', 'status', 'count_seats')
    column_labels = {"title": "Название",
                    "start": "Дата начала",
                    "course": "Предмет по которому группа",
                    "seats": "Количество мест в группе",
                    "status": "Статус",
                    "count_seats": "Набрано"}
    create_modal = True
    edit_modal = True
    
    #column_list='(count_seats','Набрано')



class MyApplicantView(ModelView, BaseModelView):
    column_exclude_list=('phone', )
    column_labels = dict(name='Имя и Фамилия',
                        mail='Почта',
                        group='Группа, в которую он записался',
                        status='Оплачено ли участие')


admin = Admin(app, template_mode='bootstrap3', index_view=DashboardView(name='Главная'), name='Stepik CRM')
admin.add_view(MyUserView(User, db.session, name='Пользователи'))
admin.add_view(MyGroupView(Group, db.session, name='Группы'))
admin.add_view(MyApplicantView(Applicant, db.session, name='Заявки'))