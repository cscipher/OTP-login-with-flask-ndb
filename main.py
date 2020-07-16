import os
from flask import Flask
from google.cloud import ndb
from flask_login import LoginManager


app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'otp-prot-14ea8863b8f1.json'
app.config['SECRET_KEY'] = 'kuyrgfurbgwkethgbt' 
app.config['ENV'] = 'development'

client = ndb.Client()



login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from models import logintable
@login_manager.user_loader
def load_user(email):
    with client.context():
        return logintable.query().filter(logintable.email==email).get()

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



    