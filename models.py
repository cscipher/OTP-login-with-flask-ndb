from google.cloud import ndb
from flask_login import UserMixin

class logintable(UserMixin, ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    otp = ndb.IntegerProperty()

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False