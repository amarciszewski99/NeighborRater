from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import User, Address, UserToAddress, Rating

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/testDB')
def testDB():

    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    #Create User objects
    userA = User(id=1, first_name='A', last_name='a', email='userA@example.com')
    db.session.add(userA)

    userB = User(id=2, first_name='B', last_name='b', email='userB@example.com')
    db.session.add(userB)

    userC = User(id=3, first_name='C', last_name='c', email='userC@example.com')
    db.session.add(userC)

    #Create Address objects
    address1 = Address(id=1, street_address='1 Address Lane')
    db.session.add(address1)

    address2 = Address(id=2, street_address='2 Address Lane')
    db.session.add(address2)

    address3 = Address(id=3, street_address='3 Address Lane')
    db.session.add(address3)

    address4 = Address(id=4, street_address='4 Address Lane')
    db.session.add(address4)

    address5 = Address(id=5, street_address='5 Address Lane')
    db.session.add(address5)

    #Create UserToAddress objects
    u2a_A1 = UserToAddress(id=1, user_id=1, address_id=1)
    db.session.add(u2a_A1)

    u2a_A2 = UserToAddress(id=2, user_id=1, address_id=2)
    db.session.add(u2a_A2)

    u2a_B2 = UserToAddress(id=3, user_id=2, address_id=2)
    db.session.add(u2a_B2)

    u2a_B3 = UserToAddress(id=4, user_id=2, address_id=3)
    db.session.add(u2a_B3)

    u2a_B4 = UserToAddress(id=5, user_id=2, address_id=4)
    db.session.add(u2a_B4)

    u2a_C5 = UserToAddress(id=6, user_id=3, address_id=5)
    db.session.add(u2a_C5)

    #Commit the session
    db.session.commit()

    userList = db.session.query(User).all()
    addressList = db.session.query(Address).all()

    return render_template('testDB.html', userList=userList, addressList=addressList)