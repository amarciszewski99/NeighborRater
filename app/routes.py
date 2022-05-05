from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Address, Profile, Rating, ProfileToAddress
from werkzeug.urls import url_parse
from datetime import date


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Welcome to NeighborRater!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_db', methods=['GET', 'POST'])
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()


    # USER
    user1 = User(id=1, name="Adam Marciszewski", email="adam@adam.com")
    user1.set_password("1234")
    db.session.add(user1)

    test_user = User(id=2, name="Test Dummy", email="test@test.com")
    test_user.set_password("test")
    db.session.add(test_user)


    # ADDRESS
    address1a = Address(id=1, housing_type="House", street_address="9 Pheasant Run", township="Holmdel",
                        state="New Jersey", zip_code="07733")
    db.session.add(address1a)
    address1b = Address(id=2, housing_type="Apartment", street_address="902 Dryden Road", township="Ithaca",
                        state="New York", zip_code="14850")
    db.session.add(address1b)

    test_address = Address(id=3, housing_type="Campus", street_address="953 Danby Road", township="Ithaca",
                           state="New York", zip_code="14850")
    db.session.add(test_address)


    # PROFILE
    profile1 = Profile(id=1, name="Adam J Marciszewski", age=22, gender="Male", birthday=date(1999, 11, 16),
                       average_rating=4.5, is_claimed=True, job_title="Software Engineer",
                       political_affiliation="Unaffiliated", user_id=1)
    db.session.add(profile1)

    test_profile = Profile(id=2, name="Test Dummy", age=18, gender="Male", birthday=date(2004, 5, 1),
                           average_rating=3.5, is_claimed=False, job_title="Test Dummy",
                           political_affiliation="Unaffiliated", user_id=2)
    db.session.add(test_profile)

    # RATING
    rating1a = Rating(id=1, rating=5.0, description="The coolest dude on the planet?")
    db.session.add(rating1a)
    rating1b = Rating(id=2, rating=4.0, description="Will NOT shut up. Otherwise, he's okay.")
    db.session.add(rating1b)

    test_rating1 = Rating(id=3, rating=3.0, description="Kinda dumb!")
    db.session.add(test_rating1)
    test_rating2 = Rating(id=4, rating=4.0, description="A real risk-seeker.")
    db.session.add(test_rating2)


    # PROFILE TO ADDRESS
    p2a1a = ProfileToAddress(id=1, profile_id=1, address_id=1, rating_id=1, is_current_address=True)
    db.session.add(p2a1a)
    p2a1b = ProfileToAddress(id=2, profile_id=1, address_id=2, rating_id=2, is_current_address=False)
    db.session.add(p2a1b)

    test_p2a = ProfileToAddress(id=3, profile_id=2, address_id=3, rating_id=3, is_current_address=True)
    db.session.add(test_p2a)

    db.session.commit()
    return render_template('reset_db.html')

