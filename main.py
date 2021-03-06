from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


from forms.ad import AdForm
from forms.user import RegisterForm, LoginForm
from data.ad import Ad
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/works.db")
    app.run()


@app.route('/ad', methods=['GET', 'POST'])
@login_required
def add_ad():
    form = AdForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ad = Ad()
        ad.title = form.title.data
        ad.phone_number = form.phone_number.data
        ad.salary = form.salary.data
        ad.content = form.content.data
        current_user.ad.append(ad)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ad.html', title='Добавление объявления по работе', form=form)

# dadad
@app.route('/ad_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ad_delete(id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).filter(Ad.id == id, Ad.user == current_user).first()
    if ad:
        db_sess.delete(ad)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/ad/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ad(id):
    form = AdForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id, Ad.user == current_user).first()
        if ad:
            form.title.data = ad.title
            form.content.data = ad.content
            form.phone_number.data = ad.phone_number
            form.salary.data = ad.salary
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id, Ad.user == current_user).first()
        if ad:
            ad.title = form.title.data
            ad.phone_number = form.phone_number.data
            ad.salary = form.salary.data
            ad.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('ad.html', title='Редактирование объявления', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).all()
    return render_template("index.html", ad=ad)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname = form.surname.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
