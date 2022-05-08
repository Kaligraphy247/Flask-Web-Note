from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user
)
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db



auth = Blueprint(name='auth', import_name=__name__)






@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data = request.form
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # get specific data from the User col in db
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(pwhash=user.password, password=password):
                flash(message="Logged in successfully! 😇", category='success')
                login_user(user=user, remember=True)
                return redirect(location=url_for('views.home_view'))
            else:
                flash(message="Incorrect password, try again 🙃", category='error')
        else:
            flash(message="Email does not exist! 🙃", category="error")

    return render_template(template_name_or_list="login.html", user=current_user)



@auth.route('/logout')
@login_required # make sure user is logged in to acces this page
def logout():
    logout_user()
    return redirect(location=url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        password_validation = request.form.get('password_validation')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists! 🙃", category="error")
        elif len(email) < 4:
            flash(message="Email must be greater than 4 characters", category='error')

        elif len(first_name) <2:
            flash(message="First Name must be greater than 1 character", category='error')

        elif len(password) < 8:
            flash(message="Password must be 8 characters or more", category='error')

        elif password != password_validation:
            flash(message="Passwords don\"t match!", category='error')
        else:
            # add user to db
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password=password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=user, remember=True)
            flash(message="Account created!", category='success')
            flash(message="You are loggind in", category='success')
            return redirect(location=url_for('views.home_view'))

    return render_template(template_name_or_list="sign_up.html", user=current_user)

