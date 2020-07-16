from flask import Blueprint, url_for, render_template , request, redirect, session
from models import logintable
from google.cloud import ndb
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from random import randrange
from mail import sendmail


auth = Blueprint('auth',__name__)


client = ndb.Client()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    with client.context():
        if request.method=='POST':
            semail = request.form.get('getmail')
            passw = request.form.get('getpass')

            user = logintable.query(logintable.email==semail).get()

            if user:
                check_pass = user.password
                hashcheck_pass = check_password_hash(check_pass, passw)
                if hashcheck_pass==True:
                    login_user(user)
                    return redirect('/protected')
                else:
                    return render_template('login.html', check=False)
                    # return render_template('debug.html', a=semail, b=passw)
            else:
                return render_template('login.html', check=True)
                # return render_template('debug.html', a=semail, b=passw)
            
        else:
            return render_template('login.html',check=None)



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    with client.context():
        if request.method=='POST':
            semail = request.form.get('getmail')
            password = request.form.get('getpassw')
            confirm_pass = request.form.get('getpassw2')
        
            user = logintable.query(logintable.email == semail).get()
            if not user:
                if confirm_pass == password:
                    hash_pass = generate_password_hash(password, method='sha256')
                    new_signup = logintable(email=semail, password=hash_pass)
                    new_signup.put()
                    return redirect('/login')
                else:
                    return render_template('signup.html', notconfirm=True, checkmail=None)
            
            else:
                return render_template('signup.html',checkmail=user.email, inputmail=semail)
        
        else:
            user,semail = None, None
            return render_template('signup.html',checkmail=user, inputmail=semail)




def otpgenerator():
    return randrange(100000, 999999)

@auth.route('/getotp', methods=['GET','POST'])
def getotp():
    with client.context():
        if request.method == 'POST':
            otp_email = request.form.get('for_email')

            user_val = logintable.query(logintable.email==otp_email).get()

            if user_val:
                gen_otp = otpgenerator()
                user_val.otp = gen_otp
                user_val.put()
                sendmail(otp_email, gen_otp)
                return redirect('/putotp')
            else:
                return render_template('otp.html', check=False)
        
        else:
            return render_template('otp.html', check=None)



@auth.route('/putotp', methods=['GET','POST'])
def putotp():
    with client.context():
        if request.method=='POST':
            otp_enter = request.form.get('getotp')
            otp_enter = int(otp_enter)
            user_val = logintable.query(logintable.otp==otp_enter).get()
            if otp_enter == user_val.otp:
                login_user(user_val)
                user_val.otp = -1
                user_val.put()
                return redirect('/protected')
            else:
                return render_template('otp.html', check=False)
        
        return render_template('otp2.html', check=None)



@auth.route('/protected', methods=['GET','POST'])
@login_required
def pro():
    return render_template('protected.html')



@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    with client.context():
        logout_user()
        return redirect('/')


@auth.route('/', methods=['GET', 'POST'])
def red():
    return redirect('/login')